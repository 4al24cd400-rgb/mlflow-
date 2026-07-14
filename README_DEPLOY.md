# Deployment Notes

This service is now designed to deploy cleanly on Render, Railway, Fly.io, or similar platforms.

## What changed
- Removed the fragile MLflow/AWS startup dependency from the main app.
- The app now loads the local model file from the repository when available.
- The Procfile uses a valid web process entry.
- The dependency list is trimmed to the packages needed for FastAPI startup.

## Deploy steps
1. Push this folder to your GitHub repository.
2. In Render, create a Web Service pointing to this folder.
3. Set the build command to:
   - pip install -r requirements.txt
4. Set the start command to:
   - uvicorn app:app --host 0.0.0.0 --port $PORT

## Expected behavior
- The root endpoint returns a welcome message.
- The /health endpoint returns service status and model availability.
- The /predict endpoint expects a JSON body like:
  {"customerID": "7590-VHVEG"}
