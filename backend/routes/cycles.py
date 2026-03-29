from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.user import db
from models.cycle import Cycle
from risk_engine import compute_risk

cycles_bp = Blueprint("cycles", __name__, url_prefix="/api/cycles")

# Fields we accept from client for cycle log
CYCLE_FIELDS = [
    "cycle_length", "irregular_cycle", "missed_periods", "pain_level", "bleeding_duration",
    "acne", "excess_facial_hair", "hair_thinning", "dark_patches", "oily_skin",
    "weight_kg", "height_cm", "fatigue", "sugar_cravings",
    "physical_activity", "sleep_hours", "fast_food_frequency", "stress_level",
]


def _coerce_bool(v):
    if v is None:
        return False
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    v_str = str(v).lower().strip()
    return v_str in ("1", "true", "yes", "on")


def _build_cycle_data(data: dict) -> dict:
    out = {}
    
    for k in CYCLE_FIELDS:
        if k not in data:
            continue
        
        v = data[k]
        
        # Handle boolean field - always process
        if k == "irregular_cycle":
            out[k] = _coerce_bool(v)
        # Handle None - skip it
        elif v is None:
            continue
        # Handle empty string - skip it (but 0 is not empty string!)
        elif v == "":
            continue
        # Handle numeric fields - 0 is a valid value!
        else:
            try:
                if k in ("weight_kg", "height_cm", "sleep_hours"):
                    # Float fields
                    out[k] = float(v)
                elif k in ("cycle_length", "missed_periods", "pain_level", "bleeding_duration",
                           "acne", "excess_facial_hair", "hair_thinning", "dark_patches", "oily_skin",
                           "fatigue", "sugar_cravings", "physical_activity", "fast_food_frequency", "stress_level"):
                    # Integer fields - 0 is valid, so we need to check type first
                    if isinstance(v, (int, float)):
                        out[k] = int(v)
                    else:
                        out[k] = int(float(v))  # Convert string to int via float first
                else:
                    out[k] = v
            except (TypeError, ValueError):
                # Skip invalid values silently
                continue
    
    return out


@cycles_bp.route("", methods=["GET"])
@jwt_required()
def list_cycles():
    user_id = get_jwt_identity()
    cycles = Cycle.query.filter_by(user_id=user_id).order_by(Cycle.created_at.desc()).all()
    return jsonify([c.to_dict() for c in cycles])


@cycles_bp.route("", methods=["POST"])
@jwt_required()
def create_cycle():
    try:
        user_id = get_jwt_identity()
        
        # Check if request has JSON
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        cycle_data = _build_cycle_data(data)
        
        # Always include irregular_cycle if not present (default to False)
        if "irregular_cycle" not in cycle_data:
            cycle_data["irregular_cycle"] = False
        
        # Debug: Print what we received and processed
        print(f"DEBUG - Received data keys: {list(data.keys())}")
        print(f"DEBUG - Processed cycle_data keys: {list(cycle_data.keys())}")
        print(f"DEBUG - Sample values: {dict(list(cycle_data.items())[:5])}")

        cycle = Cycle(user_id=user_id)
        for k, v in cycle_data.items():
            if hasattr(cycle, k):
                setattr(cycle, k, v)
        if cycle.height_cm and cycle.weight_kg:
            cycle.bmi = round(cycle.weight_kg / ((cycle.height_cm / 100) ** 2), 1)

        risk_result = compute_risk(cycle.to_dict())
        cycle.risk_score = risk_result["risk_score"]
        cycle.risk_level = risk_result["risk_level"]

        db.session.add(cycle)
        db.session.commit()
        return jsonify(cycle.to_dict()), 201
    except ValueError as e:
        db.session.rollback()
        print(f"DEBUG - ValueError: {str(e)}")
        return jsonify({"error": "Invalid data format", "message": f"Data validation error: {str(e)}"}), 422
    except Exception as e:
        db.session.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"DEBUG - Exception: {str(e)}")
        print(f"DEBUG - Traceback: {error_trace}")
        return jsonify({"error": str(e), "message": "Failed to create cycle record"}), 500


@cycles_bp.route("/<int:cycle_id>", methods=["GET"])
@jwt_required()
def get_cycle(cycle_id):
    user_id = get_jwt_identity()
    cycle = Cycle.query.filter_by(id=cycle_id, user_id=user_id).first()
    if not cycle:
        return jsonify({"error": "Cycle not found"}), 404
    out = cycle.to_dict()
    risk_result = compute_risk(out)
    out["category_scores"] = risk_result["category_scores"]
    out["recommendations"] = risk_result["recommendations"]
    return jsonify(out)


@cycles_bp.route("/<int:cycle_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_cycle(cycle_id):
    user_id = get_jwt_identity()
    cycle = Cycle.query.filter_by(id=cycle_id, user_id=user_id).first()
    if not cycle:
        return jsonify({"error": "Cycle not found"}), 404
    data = request.get_json() or {}
    cycle_data = _build_cycle_data(data)
    for k, v in cycle_data.items():
        if hasattr(cycle, k):
            setattr(cycle, k, v)
    if cycle.height_cm and cycle.weight_kg:
        cycle.bmi = round(cycle.weight_kg / ((cycle.height_cm / 100) ** 2), 1)
    risk_result = compute_risk(cycle.to_dict())
    cycle.risk_score = risk_result["risk_score"]
    cycle.risk_level = risk_result["risk_level"]
    db.session.commit()
    return jsonify(cycle.to_dict())


@cycles_bp.route("/<int:cycle_id>", methods=["DELETE"])
@jwt_required()
def delete_cycle(cycle_id):
    user_id = get_jwt_identity()
    cycle = Cycle.query.filter_by(id=cycle_id, user_id=user_id).first()
    if not cycle:
        return jsonify({"error": "Cycle not found"}), 404
    db.session.delete(cycle)
    db.session.commit()
    return jsonify({"message": "Deleted"})


@cycles_bp.route("/risk-preview", methods=["POST"])
@jwt_required()
def risk_preview():
    """Compute risk from payload without saving (for preview)."""
    data = request.get_json() or {}
    cycle_data = _build_cycle_data(data)
    if cycle_data.get("weight_kg") and cycle_data.get("height_cm"):
        h = cycle_data["height_cm"] / 100
        cycle_data["bmi"] = round(cycle_data["weight_kg"] / (h * h), 1)
    result = compute_risk(cycle_data)
    return jsonify(result)
