# 🚀 Customer Churn Prediction API

A Machine Learning-based REST API that predicts whether a telecom customer is likely to churn using a trained Random Forest model. The project is built with **FastAPI**, **Scikit-learn**, **Docker**, and is ready for deployment on cloud platforms such as **AWS Elastic Beanstalk** or **Render**.

---

## 📌 Project Overview

Customer churn prediction helps telecom companies identify customers who are likely to discontinue their services. By predicting churn in advance, companies can take preventive actions and improve customer retention.

This project exposes a REST API where a customer is identified using a **Customer ID**, and the trained machine learning model predicts whether the customer will churn.

---

## ✨ Features

- Predict customer churn using a trained Random Forest model
- REST API built using FastAPI
- Health check endpoint
- Dockerized application
- Easy deployment on AWS Elastic Beanstalk or Render
- Clean and modular project structure

---

## 🛠️ Tech Stack

### Backend
- Python 3.11
- FastAPI
- Uvicorn

### Machine Learning
- Scikit-learn
- Pandas
- Joblib

### Deployment
- Docker
- AWS Elastic Beanstalk
- Render

---

## 📂 Project Structure

```
Customer-Churn-Prediction/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
├── .gitignore
├── config.py
│
├── registered_model/
│   └── model.pkl
│
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│
├── scripts/
│
├── tests/
│
└── images/
```

---

## 📊 Dataset

**Dataset:** IBM Telco Customer Churn Dataset

Dataset contains customer information such as:

- Gender
- Senior Citizen
- Partner
- Dependents
- Tenure
- Internet Service
- Contract Type
- Monthly Charges
- Total Charges
- Churn Status

---

## 🤖 Machine Learning Model

Model Used:

- Random Forest Classifier

The trained model is stored as:

```
registered_model/model.pkl
```

---

## ⚙️ Installation

Clone the repository

```bash
https://github.com/4al24cd400-rgb/mlflow-.git

cd YOUR_REPOSITORY
```

Create Virtual Environment

```bash
python -m venv .venv
```

Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
uvicorn app:app --reload
```

API will be available at

```
https://mlflow-5.onrender.com/
```

Swagger Documentation

```
https://mlflow-5.onrender.com/docs
```

---

## 🐳 Docker

Build Docker Image

```bash
docker build -t customer-churn-api .
```

Run Docker Container

```bash
docker run -p 8000:8000 customer-churn-api
```

---

## 📡 API Endpoints

### Home

```
GET /
```

Response

```json
{
    "message": "Customer Churn Prediction API is Running"
}
```

---

### Health Check

```
GET /health
```

Example Response

```json
{
    "status": "Healthy",
    "model_loaded": true,
    "customers": 1000
}
```

---

### Predict Customer Churn

```
POST /predict
```

Request

```json
{
    "customerID": "7590-VHVEG"
}
```

Response

```json
{
    "customerID": "7590-VHVEG",
    "prediction": "Customer Will Churn"
}
```

---

## 📈 Workflow

```
Customer Request
        │
        ▼
Receive Customer ID
        │
        ▼
Load Customer Record
        │
        ▼
Preprocess Features
        │
        ▼
Random Forest Model
        │
        ▼
Prediction
        │
        ▼
JSON Response
```

---

## 📦 Requirements

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
pandas==2.2.3
scikit-learn==1.6.1
joblib==1.5.3
pydantic==2.9.0
python-dotenv==1.2.1
```

---

## 🚀 Deployment

This project can be deployed using:

- Docker
- Render

---

## 👨‍💻 Author

**Mahesh M**

B.E. Computer Science & Engineering (Data Science)

Alva's Institute of Engineering and Technology

---

## 📄 License

This project is developed for educational and learning purposes.
