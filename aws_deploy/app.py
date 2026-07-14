import os
import pandas as pd
import mlflow.pyfunc

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from download_from_s3 import download_folder


app = FastAPI(title="Customer Churn Prediction API")

MODEL_PATH = "registered_model"
DATASET_PATH = "WA_Fn-UseC_-Telco-Customer-Churn.csv"


# --------------------------------------------------
# DOWNLOAD MODEL
# --------------------------------------------------

if not os.path.exists(MODEL_PATH):
    print("Downloading model from S3...")
    download_folder()


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

try:
    model = mlflow.pyfunc.load_model(MODEL_PATH)

    sklearn_model = model._model_impl.sklearn_model

    model_features = list(
        sklearn_model.feature_names_in_
    )

    print("Model loaded successfully!")
    print("Model features:", len(model_features))

except Exception as e:
    print("Model loading failed:", e)

    model = None
    model_features = []


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

dataset = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")


# --------------------------------------------------
# PREPARE DATA
# --------------------------------------------------

X = dataset.drop(
    columns=["customerID", "Churn"]
)


# Check how model was trained
if "TotalCharges" in model_features:

    print("TotalCharges is NUMERIC")

    X["TotalCharges"] = pd.to_numeric(
        X["TotalCharges"],
        errors="coerce"
    )

    X["TotalCharges"] = X["TotalCharges"].fillna(
        X["TotalCharges"].median()
    )


# Encode categorical columns
X_encoded = pd.get_dummies(X)


# Match exact model features
X_encoded = X_encoded.reindex(
    columns=model_features,
    fill_value=0
)


print("Dataset preprocessing completed!")


# --------------------------------------------------
# INPUT
# --------------------------------------------------

class CustomerRequest(BaseModel):
    customerID: str


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Customer Churn Prediction API is Running"
    }


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "Healthy",
        "model_loaded": model is not None,
        "total_customers": len(dataset)
    }


# --------------------------------------------------
# PREDICT
# --------------------------------------------------

@app.post("/predict")
def predict(data: CustomerRequest):

    if model is None:

        raise HTTPException(
            status_code=500,
            detail="Model is not loaded"
        )


    # Find customer
    customer = dataset[
        dataset["customerID"] == data.customerID
    ]


    if customer.empty:

        raise HTTPException(
            status_code=404,
            detail="Customer ID not found"
        )


    try:

        # Get customer index
        customer_index = customer.index[0]


        # Get prepared customer data
        customer_input = X_encoded.loc[
            [customer_index]
        ]


        # Predict
        prediction = model.predict(
            customer_input
        )


        prediction_value = prediction[0]


        if str(prediction_value).lower() in [
            "1",
            "yes",
            "true"
        ]:

            result = "Customer Will Churn"

        else:

            result = "Customer Will Not Churn"


        return {
            "customerID": data.customerID,
            "prediction": result
        }


    except Exception as e:

        print("Prediction Error:", e)

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )