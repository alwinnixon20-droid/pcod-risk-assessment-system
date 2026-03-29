from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.cycle import Cycle

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")


@analytics_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    """Dashboard summary: total cycles, latest risk, cycle lengths for chart."""
    user_id = get_jwt_identity()
    cycles = Cycle.query.filter_by(user_id=user_id).order_by(Cycle.created_at.desc()).limit(50).all()
    total = Cycle.query.filter_by(user_id=user_id).count()
    latest = cycles[0] if cycles else None
    cycle_lengths = [
        {"created_at": c.created_at.isoformat() if c.created_at else None, "cycle_length": c.cycle_length}
        for c in reversed(cycles)
        if c.cycle_length is not None
    ]
    risk_progression = [
        {"created_at": c.created_at.isoformat() if c.created_at else None, "risk_score": c.risk_score, "risk_level": c.risk_level}
        for c in reversed(cycles)
        if c.risk_score is not None
    ]
    return jsonify({
        "total_cycles": total,
        "latest_risk_score": latest.risk_score if latest else None,
        "latest_risk_level": latest.risk_level if latest else None,
        "cycle_lengths": cycle_lengths,
        "risk_progression": risk_progression,
    })
