from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime


# 🔧 DB Setup
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://Mukund:1605@localhost/agriai"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DiseaseLog(Base):
    __tablename__ = "disease_logs"

    id = Column(Integer, primary_key=True, index=True)
    # Matching the actual database schema
    image_name = Column(String(255), nullable=False)
    predicted_class = Column(String(100), nullable=False)  # This is what's actually in the database
    timestamp = Column(DateTime, default=datetime.utcnow)

# 📦 Crop Prediction Table
class CropPrediction(Base):
    __tablename__ = 'crop_predictions'
    id = Column(Integer, primary_key=True, index=True)
    soil_condition = Column(String, index=True)
    weather = Column(String, index=True)
    region = Column(String, index=True)
    prediction = Column(String)

# 👤 User Data Table
class UserData(Base):
    __tablename__ = 'user_data'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    location = Column(String)
    soil_quality = Column(String)
    crop_history = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# 🧪 Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 💾 Save function
def save_crop_prediction(soil_condition: str, weather: str, region: str, prediction: str, db: Session):
    db_prediction = CropPrediction(
        soil_condition=soil_condition,
        weather=weather,
        region=region,
        prediction=prediction
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction
