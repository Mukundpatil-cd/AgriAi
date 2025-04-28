# app/models/crop_model.py

class CropModel:
    def predict_crop(self, soil_type: str, rainfall: float, temperature: float, humidity: float):
        # Yahan pe model logic add karo
        # For now, let's assume a simple rule-based prediction:
        if soil_type == "Loamy" and rainfall > 100 and temperature > 20:
            return "Rice"
        elif soil_type == "Sandy" and rainfall < 50 and temperature > 25:
            return "Wheat"
        else:
            return "Corn"
