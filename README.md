# Customer Churn Prediction API

This folder contains a FastAPI service for customer churn prediction.

## Deployment on Render

This app is ready to be deployed on Render.

### Prerequisites
- A GitHub repository containing this folder
- A Render account

### Deploy steps
1. Push this folder to GitHub.
2. Open Render and create a new Web Service.
3. Connect your GitHub repository.
4. Select the folder containing this app as the root directory.
5. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Click Deploy.

### Important notes
- The app loads the model from the `registered_model` folder.
- The service does not depend on AWS or MLflow during startup anymore.
- The app is designed to run correctly on a fresh deployment.

### API Endpoints
- `GET /` → Welcome message
- `GET /health` → Health check
- `POST /predict` → Predict churn for a customer

### Example request
```json
{
  "customerID": "7590-VHVEG"
}
```

### Example response
```json
{
  "customerID": "7590-VHVEG",
  "prediction": "Customer Will Not Churn"
}
```

### Local run
```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```
