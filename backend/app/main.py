import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.routes import crop
from app.routes.user_data import router as save_user_data_router

app = FastAPI(
    title="AgriAI Crop Prediction API",
    version="1.0.0",
    description="An API to predict the best crop based on soil and weather conditions."
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

# ✅ Root endpoint
@app.get("/")
def read_root():
    return {"message": "🌿 AgriAI API is up and running!"}
