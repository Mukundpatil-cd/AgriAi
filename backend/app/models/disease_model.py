# app/models/disease_model.py

from pydantic import BaseModel

class DiseaseModel(BaseModel):
    disease_name: str  # Disease ka naam
    symptoms: str      # Symptoms ka description
    treatment: str     # Disease ka treatment

    class Config:
        from_attributes = True  # Pydantic V2 ke liye updated configuration
