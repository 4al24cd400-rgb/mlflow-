import os
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Customer Churn Prediction API")

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "registered_model" / "model.pkl"
DATASET_PATH = BASE_DIR / "WA_Fn-UseC_-Telco-Customer-Churn.csv"


class CustomerRequest(BaseModel):
    customerID: str


def load_model():
    if MODEL_PATH.exists():
        try:
            model = joblib.load(MODEL_PATH)
            print("Model loaded successfully!")
            return model
        except Exception as exc:
            print("Model loading failed:", exc)

    print("Model file not found. Starting without a model.")
    return None


def prepare_dataset():
    dataset = pd.read_csv(DATASET_PATH)
    print("Dataset loaded successfully!")

    features = dataset.drop(columns=["customerID", "Churn"]).copy()
    features["TotalCharges"] = pd.to_numeric(features["TotalCharges"], errors="coerce")
    features["TotalCharges"] = features["TotalCharges"].fillna(features["TotalCharges"].median())

    encoded = pd.get_dummies(features)
    encoded.index = dataset.index
    return dataset, encoded


model = load_model()
dataset, X_encoded = prepare_dataset()
model_features = list(getattr(model, "feature_names_in_", X_encoded.columns))
X_encoded = X_encoded.reindex(columns=model_features, fill_value=0)
print("Dataset preprocessing completed!")


@app.get("/")
def home():
    return {"message": "Customer Churn Prediction API is Running"}


@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "model_loaded": model is not None,
        "total_customers": len(dataset),
    }


@app.post("/predict")
def predict(data: CustomerRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")

    customer = dataset[dataset["customerID"] == data.customerID]

    if customer.empty:
        raise HTTPException(status_code=404, detail="Customer ID not found")

    try:
        customer_index = customer.index[0]
        customer_input = X_encoded.loc[[customer_index]]
        prediction = model.predict(customer_input)
        prediction_value = prediction[0]

        result = (
            "Customer Will Churn"
            if str(prediction_value).lower() in ["1", "yes", "true"]
            else "Customer Will Not Churn"
        )

        return {"customerID": data.customerID, "prediction": result}

    except Exception as exc:
        print("Prediction Error:", exc)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(exc)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)
