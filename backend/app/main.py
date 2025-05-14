import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.routes import crop
from app.routes.user_data import router as save_user_data_router
from app.routes.disease import router as disease_router

# Import database components
from app.database import Base, engine

# Create all tables
print("Ensuring database tables exist...")
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgriAI Crop Prediction API",
    version="1.0.0",
    description="An API to predict the best crop based on soil and weather conditions."
)

from fastapi.middleware.cors import CORSMiddleware

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(crop.router, tags=["Crop Prediction"])
app.include_router(save_user_data_router, tags=["User Data"])
app.include_router(disease_router, tags=["Disease Detection"])

# ✅ Root endpoint
@app.get("/")
def read_root():
    return {"message": "🌿 AgriAI API is up and running!"}
