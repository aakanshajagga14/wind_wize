import joblib
import os
import numpy as np
import requests


model_path = os.path.join("backend", "wind_orientation_model.pkl")
model = joblib.load(model_path)

def get_wind_direction(latitude, longitude):
    """Fetch the real wind direction using OpenWeatherMap API"""
    api_key = "7beae662d05b058f7bbb2c379d8cc9dd" 
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    
    if response.get("wind"):
        return response["wind"]["deg"] 
    else:
        return None

def predict_orientation(latitude, longitude, wind_speed):
    """
    Predicts the optimal wind turbine orientation based on wind speed and location data.
    """
    if wind_speed > 0:
        wind_direction = get_wind_direction(latitude, longitude)
        if wind_direction is None:
            wind_direction = (latitude + longitude) % 360 
        
        temperature = 25.0 
        humidity = 50.0  
        
        features = np.array([[wind_speed, wind_direction, temperature, humidity]])
        

        orientation = model.predict(features)[0]  
        
        return round(orientation, 2)  
    
    return "N/A" 
