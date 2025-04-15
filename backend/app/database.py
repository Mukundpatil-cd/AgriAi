from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://Mukund:1605@localhost/agriai"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the database model
class CropPrediction(Base):
    __tablename__ = 'crop_predictions'
    id = Column(Integer, primary_key=True, index=True)
    soil_condition = Column(String, index=True)
    weather = Column(String, index=True)
    region = Column(String, index=True)
    prediction = Column(String)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to save crop prediction to the database
def save_crop_prediction(soil_condition: str, weather: str, region: str, prediction: str, db: Session):
    db_prediction = CropPrediction(soil_condition=soil_condition, weather=weather, region=region, prediction=prediction)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

# Create the tables in the database
Base.metadata.create_all(bind=engine)
