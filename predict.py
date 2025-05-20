from flask import Flask, request, jsonify
import numpy as np
import joblib


app = Flask(__name__)


model = joblib.load("model.pkl")  

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() 
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    wind_speed = data.get('wind_speed')
    wind_direction = data.get('wind_direction')

    
    print(f"Received Data: latitude={latitude}, longitude={longitude}, wind_speed={wind_speed}, wind_direction={wind_direction}")

    
    orientation = predict_orientation(latitude, longitude, wind_speed, wind_direction)

    
    print(f"Predicted Orientation: {orientation}")

    return jsonify({"orientation": orientation})

def predict_orientation(latitude, longitude, wind_speed, wind_direction):
    
    base_orientation = wind_direction + (wind_speed * 0.1)
    base_orientation = base_orientation % 360
    adjusted_orientation = base_orientation + (latitude / 100)
    adjusted_orientation = adjusted_orientation % 360
    
    return round(adjusted_orientation, 2)

if __name__ == '__main__':
    app.run(debug=True)
