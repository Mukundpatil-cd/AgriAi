from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.crop import CropRequest, CropResponse
from app.database import SessionLocal, get_db, save_crop_prediction, UserData
from app.utils.model_utils import evaluate_model

import joblib
import os
import numpy as np

router = APIRouter()

model = None

# Function to lazily load the model only when it's needed
def get_model():
    global model
    if model is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "crop_model.pkl")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at: {model_path}")
        model = joblib.load(model_path)
    return model

@router.post("/predict-crop", response_model=CropResponse)
def predict_crop(data: CropRequest, db: Session = Depends(get_db)):
    # Step 1: Evaluate the model for performance
    is_model_good = evaluate_model()
    if not is_model_good:
        raise HTTPException(status_code=500, detail="Model accuracy is below threshold")
    
    # Step 2: Optional: Check if user data exists
    user_data = db.query(UserData).filter(
        UserData.location == data.location,
        UserData.soil_quality == data.soil_quality
    ).first()

    if user_data:
        # You can log or take further action if user data is found
        print(f"Found user data: {user_data}")
    
    # Step 3: Prepare input data for prediction
    input_array = np.array([[data.N, data.P, data.K, data.temperature, data.humidity, data.ph, data.rainfall]])
    
    # Step 4: Load model and make prediction
    model = get_model()  # Ensure the model is loaded
    try:
        prediction = model.predict(input_array)[0]  # Get the predicted crop
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    # Step 5: Save the prediction to the database
    try:
        save_crop_prediction(
            soil_condition=data.soil_quality,
            weather=f"{data.temperature}-{data.humidity}",
            region=data.location,
            prediction=prediction,
            db=db
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving prediction: {str(e)}")
    
    # Step 6: Return the predicted crop along with the location and soil condition
    return {
        "crop": prediction,
        "location": data.location,
        "soil_condition": data.soil_quality
    }
