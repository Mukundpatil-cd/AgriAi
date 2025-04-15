from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging

from .database import get_db, save_crop_prediction, CropPrediction

# FastAPI instance
app = FastAPI()

# Pydantic models to accept input data
class CropInput(BaseModel):
    soil_condition: str
    weather: str
    region: str

# FastAPI Routes
@app.post("/predict-crop")
def predict_crop(input_data: CropInput, db: Session = Depends(get_db)):
    logging.debug(f"Received input data: {input_data}")
    try:
        # Replace with actual ML model prediction logic
        prediction = "Prediction result based on model"  # Placeholder
        
        # Log the prediction result
        logging.debug(f"Prediction result: {prediction}")
        
        # Save prediction to the database
        save_crop_prediction(input_data.soil_condition, input_data.weather, input_data.region, prediction, db)
        
        return {"prediction": prediction}
    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in prediction: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "API is working!"}
