import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, classification_report

# ------------------
# Load Data
# ------------------


# ------------------
# Create Classification Label
# ------------------

def waiting_category(time):
    if time <= 15:
        return "Short"
    elif time <= 30:
        return "Medium"
    else:
        return "Long"

data["waiting_category"] = data["waiting_time"].apply(waiting_category)

# ------------------
# Features
# ------------------

X = data[[
    "arrival_hour",
    "queue_length",
    "doctors_available",
    "triage_level",
    "patient_age"
]]

y_reg = data["waiting_time"]
y_cls = data["waiting_category"]

# ------------------
# Train Test Split
# ------------------

X_train, X_test, y_reg_train, y_reg_test = train_test_split(
    X, y_reg, test_size=0.2, random_state=42
)

_, _, y_cls_train, y_cls_test = train_test_split(
    X, y_cls, test_size=0.2, random_state=42
)

# ------------------
# Hyperparameter Tuning (Regression)
# ------------------

param_grid = {
    "n_estimators":[50,100,200],
    "max_depth":[None,5,10]
}

grid = GridSearchCV(
    RandomForestRegressor(),
    param_grid,
    cv=2
)

grid.fit(X_train, y_reg_train)

print("Best Parameters:", grid.best_params_)

reg_model = grid.best_estimator_

# ------------------
# Train Classification Model
# ------------------

cls_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

cls_model.fit(X_train, y_cls_train)

# ------------------
# Evaluation
# ------------------

reg_pred = reg_model.predict(X_test)

print("Regression Results")
import numpy as np

mse = mean_squared_error(y_reg_test, reg_pred)
rmse = np.sqrt(mse)

print("RMSE:", rmse)
print("R2:", r2_score(y_reg_test, reg_pred))

cls_pred = cls_model.predict(X_test)

print("\nClassification Results")
print(classification_report(y_cls_test, cls_pred))

# ------------------
# Save Models
# ------------------

joblib.dump(reg_model, "models/regression_model.pkl")
joblib.dump(cls_model, "models/classification_model.pkl")

print("Models saved successfully")