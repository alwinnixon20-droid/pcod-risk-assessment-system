import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("pcos_dataset.csv", encoding="latin1")

# 🔥 CLEAN BAD VALUES
data.replace(["#NAME?", "?", "NA", ""], pd.NA, inplace=True)

# Convert all columns to numeric if possible
data = data.apply(pd.to_numeric, errors='coerce')

# Drop rows with missing values
data = data.dropna()

# 🔥 RENAME COLUMNS (IMPORTANT)
data = data.rename(columns={
    "Cycle length(days)": "cycle_length",
    "BMI": "bmi",
    "Acne(Y/N)": "acne",
    "Hair growth(Y/N)": "hair_growth",
    "Weight gain(Y/N)": "weight_gain",
    "Fast food (Y/N)": "fast_food",
    "Exercise(Y/N)": "exercise",
    "PCOS (Y/N)": "pcos"
})

# Features & target
X = data.drop("pcos", axis=1)
y = data["pcos"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
print("Accuracy:", model.score(X_test, y_test))

# Save model
joblib.dump(model, "pcos_model.pkl")

print("✅ Model created successfully!")