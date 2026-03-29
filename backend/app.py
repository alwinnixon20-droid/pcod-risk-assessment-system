from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import numpy as np

# Safe import for ML
try:
    import joblib
except ImportError:
    joblib = None

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# -----------------------------
# DATABASE SETUP
# -----------------------------
DB_PATH = "pcos.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cycles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        cycle_length INTEGER,
        risk_score INTEGER,
        risk_level TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# -----------------------------
# MODEL LOADING
# -----------------------------
MODEL_PATH = "model.pkl"
model = None

if joblib and os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully")
    except Exception as e:
        print("⚠ Model load failed:", e)
        model = None
else:
    print("⚠ Model not found, using dummy prediction")

# -----------------------------
# DUMMY PREDICTION
# -----------------------------
def dummy_prediction(data):
    return {
        "risk_score": 50,
        "risk_level": "medium"
    }

# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def home():
    return "PCOS API running"

# -------- REGISTER --------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return jsonify({"message": "User registered successfully"})
    except:
        return jsonify({"error": "User already exists"}), 400
    finally:
        conn.close()

# -------- LOGIN --------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()

    conn.close()

    if user:
        return jsonify({"user_id": user[0]})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# -------- PREDICT --------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Use ML model if available
    if model:
        try:
            features = np.array([list(data.values())])
            pred = model.predict(features)[0]
            score = int(pred)
        except:
            score = 50
    else:
        score = 50

    # Convert score to level
    if score > 70:
        level = "high"
    elif score > 40:
        level = "medium"
    else:
        level = "low"

    return jsonify({
        "risk_score": score,
        "risk_level": level
    })

# -------- SAVE CYCLE --------
@app.route("/save-cycle", methods=["POST"])
def save_cycle():
    data = request.json

    user_id = data.get("user_id")
    cycle_length = data.get("cycle_length")
    risk_score = data.get("risk_score")
    risk_level = data.get("risk_level")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cycles (user_id, cycle_length, risk_score, risk_level)
        VALUES (?, ?, ?, ?)
    """, (user_id, cycle_length, risk_score, risk_level))

    conn.commit()
    conn.close()

    return jsonify({"message": "Cycle saved successfully"})

# -------- HISTORY --------
@app.route("/history/<int:user_id>", methods=["GET"])
def history(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT cycle_length, risk_score, risk_level, created_at
        FROM cycles
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "cycle_length": r[0],
            "risk_score": r[1],
            "risk_level": r[2],
            "created_at": r[3]
        })

    return jsonify(result)

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)