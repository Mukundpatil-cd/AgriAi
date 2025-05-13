# app/routers/user_data.py
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import UserData, SessionLocal  # Import UserData directly from database.py


router = APIRouter()

# Pydantic model to accept user input
class UserDataRequest(BaseModel):
    user_id: int
    location: str
    soil_quality: str

# API to save user data
@router.post("/save-user-data")
async def save_user_data(user_data: UserDataRequest):
    db = SessionLocal()
    new_user_data = UserData(
        user_id=user_data.user_id,
        location=user_data.location,
        soil_quality=user_data.soil_quality,
        crop_history="[]"  # Initial empty crop history
    )
    db.add(new_user_data)
    db.commit()
    return {"message": "User data saved successfully!"}

