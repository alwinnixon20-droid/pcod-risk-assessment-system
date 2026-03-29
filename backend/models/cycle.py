from .user import db
from datetime import datetime

class Cycle(db.Model):
    __tablename__ = "cycles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Menstrual pattern
    cycle_length = db.Column(db.Integer, nullable=True)  # days
    irregular_cycle = db.Column(db.Boolean, default=False)
    missed_periods = db.Column(db.Integer, default=0)
    pain_level = db.Column(db.Integer, nullable=True)  # 1-10
    bleeding_duration = db.Column(db.Integer, nullable=True)  # days

    # Physical & hormonal symptoms (0 = none, 1 = mild, 2 = moderate, 3 = severe)
    acne = db.Column(db.Integer, default=0)
    excess_facial_hair = db.Column(db.Integer, default=0)
    hair_thinning = db.Column(db.Integer, default=0)
    dark_patches = db.Column(db.Integer, default=0)
    oily_skin = db.Column(db.Integer, default=0)

    # Metabolic
    weight_kg = db.Column(db.Float, nullable=True)
    height_cm = db.Column(db.Float, nullable=True)
    bmi = db.Column(db.Float, nullable=True)  # auto-calculated
    fatigue = db.Column(db.Integer, default=0)  # 0-3
    sugar_cravings = db.Column(db.Integer, default=0)  # 0-3

    # Lifestyle
    physical_activity = db.Column(db.Integer, default=0)  # 0=sedentary, 1=light, 2=moderate, 3=active
    sleep_hours = db.Column(db.Float, nullable=True)
    fast_food_frequency = db.Column(db.Integer, default=0)  # times per week
    stress_level = db.Column(db.Integer, default=0)  # 0-3

    # Cached risk (computed by engine)
    risk_score = db.Column(db.Float, nullable=True)
    risk_level = db.Column(db.String(20), nullable=True)  # low, moderate, high

    @property
    def bmi_value(self) -> float | None:
        if self.weight_kg and self.height_cm and self.height_cm > 0:
            return round(self.weight_kg / ((self.height_cm / 100) ** 2), 1)
        return self.bmi

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "cycle_length": self.cycle_length,
            "irregular_cycle": self.irregular_cycle,
            "missed_periods": self.missed_periods,
            "pain_level": self.pain_level,
            "bleeding_duration": self.bleeding_duration,
            "acne": self.acne,
            "excess_facial_hair": self.excess_facial_hair,
            "hair_thinning": self.hair_thinning,
            "dark_patches": self.dark_patches,
            "oily_skin": self.oily_skin,
            "weight_kg": self.weight_kg,
            "height_cm": self.height_cm,
            "bmi": self.bmi_value or self.bmi,
            "fatigue": self.fatigue,
            "sugar_cravings": self.sugar_cravings,
            "physical_activity": self.physical_activity,
            "sleep_hours": self.sleep_hours,
            "fast_food_frequency": self.fast_food_frequency,
            "stress_level": self.stress_level,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
        }
