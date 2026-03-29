# PCOS/PCOD Risk Assessment System

A full-stack pattern-based menstrual health screening platform. This is a **decision-support tool**, not a diagnostic tool.

## Features

- **Authentication**: Register, login, JWT (24h expiry), protected routes
- **Dashboard**: Summary cards, cycle trend chart (Recharts), risk preview
- **Cycle logging**: Menstrual pattern, physical/hormonal symptoms, metabolic indicators (BMI), lifestyle factors
- **Risk scoring engine**: Weighted categories (Menstrual 40%, Hormonal 30%, Metabolic 20%, Lifestyle 10%), Low/Moderate/High classification, recommendations
- **Risk assessment page**: Score, progress bar, risk level, recommendations, medical disclaimer
- **History & analytics**: Cycle history list, cycle length over time, risk progression

## Tech stack

- **Frontend**: React (Vite), TypeScript, Tailwind CSS, React Router, Axios, Recharts
- **Backend**: Flask, SQLite, Flask-JWT-Extended, Flask-CORS
- **Security**: JWT, hashed passwords (Werkzeug), protected API, CORS

## Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
set FLASK_APP=app.py
python -m flask run
```

Runs at `http://localhost:5000`. Optional: set `SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL` in environment.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173`. Optional: create `.env` with `VITE_API_URL=http://localhost:5000` if the API is elsewhere.

## Disclaimer

**This platform provides early risk screening and does not replace professional medical diagnosis.** Always consult a healthcare provider for diagnosis and treatment.
