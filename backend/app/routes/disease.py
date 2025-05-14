from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import torch
from torchvision import transforms
from app.models.disease_model import DiseaseModel  # Ensure this imports your trained model
import os
from app.database import SessionLocal, DiseaseLog
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db  # Database connection utility

# Create temp directory if it doesn't exist
os.makedirs("app/temp", exist_ok=True)

router = APIRouter()

# Load the trained model
MODEL_PATH = "app/models/disease_model.pth"
model = DiseaseModel(num_classes=10)
try:
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()
except Exception as e:
    print(f"Error loading model: {e}")
    # Continue without crashing, but model won't work

# Image preprocessing transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Class names for the disease model
class_names = [
    'Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold',
    'Septoria_leaf_spot', 'Target_Spot', 'Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato_mosaic_virus', 'Two-spotted_spider_mite', 'healthy'
]

@router.post("/predict-disease")
async def predict_disease(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")  # Ensure RGB format
        
        # Apply transformation
        image_tensor = transform(image).unsqueeze(0)

        # Prediction with confidence
        with torch.no_grad():
            outputs = model(image_tensor)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probs, 1)

        predicted_class = class_names[predicted.item()]
        confidence_score = float(confidence.item())

        # Treatment mapping
        treatment_mapping = {
            'Bacterial_spot': 'Use copper-based bactericides and avoid overhead irrigation.',
            'Early_blight': 'Apply fungicides like chlorothalonil; rotate crops annually.',
            'Late_blight': 'Use fungicides like mancozeb; remove infected plants.',
            'Leaf_Mold': 'Ensure good air circulation and apply fungicides.',
            'Septoria_leaf_spot': 'Use resistant varieties and fungicides like copper-based sprays.',
            'Target_Spot': 'Remove infected leaves and apply appropriate fungicides.',
            'Tomato_Yellow_Leaf_Curl_Virus': 'Control whitefly vectors and use virus-resistant seeds.',
            'Tomato_mosaic_virus': 'Avoid handling plants too much and disinfect tools.',
            'Two-spotted_spider_mite': 'Use insecticidal soap or neem oil regularly.',
            'healthy': 'No disease detected. Maintain proper watering and nutrition.'
        }

        treatment = treatment_mapping.get(predicted_class, "No treatment available.")

        # Log prediction to database
        try:
            log = DiseaseLog(
                image_name=file.filename,
                predicted_class=predicted_class
            )
            db.add(log)
            db.commit()
            print(f"Successfully logged prediction: {predicted_class}")
        except SQLAlchemyError as db_error:
            db.rollback()
            print(f"Database error: {db_error}")

        return JSONResponse(content={
            "predicted_class": predicted_class,
            "confidence": round(confidence_score * 100, 2),
            "treatment": treatment
        })

    except Exception as e:
        print(f"Error in disease prediction: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)

# Keeping the upload endpoint for backward compatibility
@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        print("Received file:", file.filename)
        
        # Save file to temp
        contents = await file.read()
        image_path = f"app/temp/{file.filename}"
        with open(image_path, "wb") as f:
            f.write(contents)

        # Open and transform the image
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = transform(image).unsqueeze(0)

        # Predict
        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)

        predicted_class = class_names[predicted.item()]        # Save to DB
        log = DiseaseLog(
            image_name=file.filename,
            predicted_class=predicted_class  # Using the correct column name
        )
        db.add(log)
        db.commit()
        print(f"Prediction saved to database: {predicted_class}")

        return {"message": "File uploaded and prediction saved!", "prediction": predicted_class}

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
        return {"error": f"Database error: {str(e)}"}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
