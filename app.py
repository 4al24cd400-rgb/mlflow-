import os
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0.0"
)

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "registered_model" / "model.pkl"
DATASET_PATH = BASE_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

# -------------------------------------------------------
# Request Model
# -------------------------------------------------------

class CustomerRequest(BaseModel):
    customerID: str


# -------------------------------------------------------
# Load Model
# -------------------------------------------------------

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    return joblib.load(MODEL_PATH)


# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

def load_dataset():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)

    features = df.drop(columns=["customerID", "Churn"]).copy()

    features["TotalCharges"] = pd.to_numeric(
        features["TotalCharges"],
        errors="coerce"
    )

    features["TotalCharges"] = features["TotalCharges"].fillna(
        features["TotalCharges"].median()
    )

    encoded = pd.get_dummies(features)

    return df, encoded


# -------------------------------------------------------
# Startup
# -------------------------------------------------------

try:
    model = load_model()
    dataset, X_encoded = load_dataset()

    feature_order = list(
        getattr(model, "feature_names_in_", X_encoded.columns)
    )

    X_encoded = X_encoded.reindex(
        columns=feature_order,
        fill_value=0
    )

    print("Application started successfully.")

except Exception as e:
    print(e)
    model = None
    dataset = None
    X_encoded = None


# -------------------------------------------------------
# Routes
# -------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is Running"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy" if model is not None else "Model Not Loaded",
        "model_loaded": model is not None,
        "customers": 0 if dataset is None else len(dataset)
    }


@app.post("/predict")
def predict(request: CustomerRequest):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded."
        )

    customer = dataset[
        dataset["customerID"] == request.customerID
    ]

    if customer.empty:
        raise HTTPException(
            status_code=404,
            detail="Customer ID not found."
        )

    index = customer.index[0]

    sample = X_encoded.loc[[index]]

    prediction = model.predict(sample)[0]

    if str(prediction).lower() in ["1", "yes", "true"]:
        result = "Customer Will Churn"
    else:
        result = "Customer Will Not Churn"

    return {
        "customerID": request.customerID,
        "prediction": result
    }


# -------------------------------------------------------
# Run
# -------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False,
    )
