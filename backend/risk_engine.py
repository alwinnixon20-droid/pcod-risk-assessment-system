"""
PCOS/PCOD Risk Scoring Engine (Decision-Support Only).
Uses weighted categories: Menstrual 40%, Hormonal 30%, Metabolic 20%, Lifestyle 10%.
Does NOT provide medical diagnosis.
"""

from typing import Any

# Category weights (must sum to 100)
WEIGHT_MENSTRUAL = 0.40
WEIGHT_HORMONAL = 0.30
WEIGHT_METABOLIC = 0.20
WEIGHT_LIFESTYLE = 0.10

# Max sub-scores per category (0-100 scale per category, then weighted)
MAX_MENSTRUAL = 100
MAX_HORMONAL = 100
MAX_METABOLIC = 100
MAX_LIFESTYLE = 100


def _menstrual_score(data: dict[str, Any]) -> float:
    """Menstrual pattern sub-score 0-100."""
    score = 0.0
    # Cycle length: 21-35 normal; <21 or >35 or missing adds risk
    cl = data.get("cycle_length")
    if cl is not None:
        if cl < 21 or cl > 35:
            score += 30
        elif cl < 25 or cl > 31:
            score += 15
    else:
        score += 10  # missing data
    # Irregular cycle
    if data.get("irregular_cycle"):
        score += 25
    # Missed periods
    missed = data.get("missed_periods") or 0
    score += min(missed * 8, 25)
    # Pain level 1-10 -> up to 20
    pain = data.get("pain_level")
    if pain is not None:
        score += (pain / 10) * 20
    # Bleeding duration: 2-7 normal; <2 or >7 adds risk
    bd = data.get("bleeding_duration")
    if bd is not None and (bd < 2 or bd > 7):
        score += 15
    return min(score, MAX_MENSTRUAL)


def _hormonal_score(data: dict[str, Any]) -> float:
    """Hormonal/physical symptoms sub-score 0-100. Severity 0-3 each."""
    items = [
        data.get("acne", 0),
        data.get("excess_facial_hair", 0),
        data.get("hair_thinning", 0),
        data.get("dark_patches", 0),
        data.get("oily_skin", 0),
    ]
    # Each 0-3, 5 items -> max 15; scale to 100
    total = sum(items)
    return min((total / 15) * 100, MAX_HORMONAL)


def _metabolic_score(data: dict[str, Any]) -> float:
    """Metabolic sub-score 0-100: BMI + fatigue + sugar cravings."""
    score = 0.0
    bmi = data.get("bmi")
    if bmi is not None:
        if bmi >= 30:
            score += 45
        elif bmi >= 25:
            score += 25
        elif bmi >= 23:
            score += 10
    score += (data.get("fatigue", 0) / 3) * 25
    score += (data.get("sugar_cravings", 0) / 3) * 30
    return min(score, MAX_METABOLIC)


def _lifestyle_score(data: dict[str, Any]) -> float:
    """Lifestyle sub-score 0-100 (higher = worse)."""
    score = 0.0
    # Physical activity: 0 sedentary -> high risk, 3 active -> low
    pa = data.get("physical_activity", 0)
    score += (3 - pa) / 3 * 30
    # Sleep: <6 or >9 adds risk
    sleep = data.get("sleep_hours")
    if sleep is not None:
        if sleep < 6 or sleep > 9:
            score += 25
        elif sleep < 7 or sleep > 8:
            score += 10
    # Fast food
    ff = data.get("fast_food_frequency", 0)
    score += min(ff * 5, 25)
    # Stress 0-3
    score += (data.get("stress_level", 0) / 3) * 25
    return min(score, MAX_LIFESTYLE)


def _total_score(menstrual: float, hormonal: float, metabolic: float, lifestyle: float) -> float:
    return (
        menstrual * WEIGHT_MENSTRUAL
        + hormonal * WEIGHT_HORMONAL
        + metabolic * WEIGHT_METABOLIC
        + lifestyle * WEIGHT_LIFESTYLE
    )


def _risk_level(score: float) -> str:
    if score < 35:
        return "low"
    if score < 65:
        return "moderate"
    return "high"


def _recommendations(score: float, level: str, data: dict[str, Any]) -> list[str]:
    recs = []
    if level == "high":
        recs.append("Consider discussing your symptoms with a healthcare provider for proper evaluation.")
    recs.append("This screening does not replace professional medical diagnosis.")
    if data.get("irregular_cycle"):
        recs.append("Tracking cycles regularly can help you and your doctor identify patterns.")
    if (data.get("bmi") or 0) >= 25:
        recs.append("Healthy diet and regular physical activity may support overall metabolic health.")
    if (data.get("physical_activity") or 0) <= 1:
        recs.append("Gradual increase in physical activity, as advised by your doctor, can be beneficial.")
    if (data.get("sleep_hours") or 0) and (data.get("sleep_hours") or 0) < 7:
        recs.append("Aim for 7–8 hours of sleep; good sleep supports hormonal balance.")
    if (data.get("stress_level") or 0) >= 2:
        recs.append("Stress management techniques may help; consider speaking with a counselor if needed.")
    return recs


def compute_risk(cycle_data: dict[str, Any]) -> dict[str, Any]:
    """
    Compute risk score and level from a single cycle/symptom record.
    cycle_data: dict with keys matching Cycle model (cycle_length, irregular_cycle, etc.).
    BMI can be passed as 'bmi' or computed from weight_kg and height_cm.
    """
    data = dict(cycle_data)
    if data.get("bmi") is None and data.get("weight_kg") and data.get("height_cm"):
        h = data["height_cm"] / 100
        data["bmi"] = round(data["weight_kg"] / (h * h), 1)

    menstrual = _menstrual_score(data)
    hormonal = _hormonal_score(data)
    metabolic = _metabolic_score(data)
    lifestyle = _lifestyle_score(data)
    total = _total_score(menstrual, hormonal, metabolic, lifestyle)
    level = _risk_level(total)
    recs = _recommendations(total, level, data)

    return {
        "risk_score": round(total, 1),
        "risk_level": level,
        "category_scores": {
            "menstrual": round(menstrual, 1),
            "hormonal": round(hormonal, 1),
            "metabolic": round(metabolic, 1),
            "lifestyle": round(lifestyle, 1),
        },
        "recommendations": recs,
    }
