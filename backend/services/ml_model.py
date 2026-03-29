import joblib

model = joblib.load("pcos_model.pkl")

def predict_risk(features):
    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0][1]
    return prediction, probability