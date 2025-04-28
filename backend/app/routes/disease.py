from fastapi import APIRouter
from pydantic import BaseModel
from app.models.disease_model import DiseaseModel  # Absolute import
 # Disease model import karo

router = APIRouter()

class DiseaseData(BaseModel):
    image: str  # Assume that image will be provided as a base64 string

@router.post("/predict-disease")
async def predict_disease(disease_data: DiseaseData):
    # Disease detection model ko call karo
    disease_model = DiseaseModel()  # Model ko initialize karo
    result = disease_model.predict(disease_data.image)  # Prediction karo
    return {"prediction": result}
