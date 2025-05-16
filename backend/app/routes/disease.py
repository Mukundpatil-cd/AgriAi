from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import torch
from torchvision import transforms
from app.models.disease_model import DiseaseModel
import os
import random
import string
from app.database import SessionLocal, DiseaseLog
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db

# Create temp directory if it doesn't exist
os.makedirs("app/temp", exist_ok=True)
os.makedirs("app/secure_images", exist_ok=True)  # Secure folder for storing images

# Allowed file types and max size (5MB)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

router = APIRouter()

# Load the trained model
MODEL_PATH = "app/models/disease_model.pth"
model = DiseaseModel(num_classes=10)
try:
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()
except Exception as e:
    print(f"Error loading model: {e}")

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Disease class labels
class_names = [
    'Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold',
    'Septoria_leaf_spot', 'Target_Spot', 'Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato_mosaic_virus', 'Two-spotted_spider_mite', 'healthy'
]

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

# Helper function for file type validation
def allowed_file(filename: str) -> bool:
    if not filename or '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

# Helper function for generating random filename
def generate_random_filename(extension: str) -> str:
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return f"{random_string}.{extension}"

@router.post("/predict-disease")
async def predict_disease(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        print(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        # File type validation
        if not allowed_file(file.filename):
            print(f"File validation failed: {file.filename}")
            if '.' not in file.filename:
                print("File has no extension")
            else:
                ext = file.filename.rsplit('.', 1)[1].lower()
                print(f"Extension: {ext}, Allowed: {ext in ALLOWED_EXTENSIONS}")
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, JPEG, PNG are allowed.")

        # File size validation
        file_size = len(await file.read())
        print(f"File size: {file_size} bytes")
        if file_size > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=400, detail="File is too large. Maximum size allowed is 5MB.")
        
        # Reset file pointer after reading for validation
        await file.seek(0)

        # Save the file securely with random name
        extension = file.filename.rsplit('.', 1)[1].lower()
        secure_filename = generate_random_filename(extension)
        save_path = os.path.join("app/secure_images", secure_filename)

        # Save the image to disk
        with open(save_path, "wb") as buffer:
            buffer.write(await file.read())

        # Read and transform image
        image = Image.open(save_path).convert("RGB")
        image_tensor = transform(image).unsqueeze(0)

        # Predict and get confidence
        with torch.no_grad():
            outputs = model(image_tensor)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probs, 1)

        predicted_class = class_names[predicted.item()]
        confidence_score = float(confidence.item())
        treatment = treatment_mapping.get(predicted_class, "No treatment available.")

        # Log prediction to database
        try:
            log = DiseaseLog(
                image_name=file.filename,
                predicted_class=predicted_class
            )
            db.add(log)
            db.commit()
            print(f"Prediction logged: {predicted_class}")
        except SQLAlchemyError as db_error:
            db.rollback()
            print(f"Database error: {db_error}")

        return JSONResponse(content={
            "predicted_class": predicted_class,
            "confidence": round(confidence_score * 100, 2),
            "treatment": treatment
        })

    except Exception as e:
        print(f"Prediction error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)
