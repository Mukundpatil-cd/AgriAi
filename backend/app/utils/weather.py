import requests
import os

# OpenWeatherMap API key (replace with your actual API key)
API_KEY = "7cbba7d09a6720a3048edc84f5b386f2"  # Yahan apni API key daalna

# Weather API URL
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city: str):
    """Fetch real-time weather data"""
    params = {
        "q": city,  # City name
        "appid": API_KEY,  # Your API key
        "units": "metric"  # To get temperature in Celsius
    }
    
    # Sending the request to the API
    response = requests.get(BASE_URL, params=params)
    
    # Checking if request was successful
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "temperature": data["main"]["temp"],  # Temperature in Celsius
            "humidity": data["main"]["humidity"],  # Humidity percentage
            "rainfall": data["rain"]["1h"] if "rain" in data else 0  # Rainfall (if available)
        }
        return weather_info
    else:
        print(f"Error: {response.status_code}")
        return None
