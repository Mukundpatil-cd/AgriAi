from app.database import Base, engine

from app.database import DiseaseLog  # Make sure DiseaseLog is defined in database.py

print("📦 Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Done.")
