from flask import Flask, request, jsonify
import numpy as np
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained model
model = joblib.load("model.pkl")  # Adjust path as necessary

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get JSON data from frontend
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    wind_speed = data.get('wind_speed')
    wind_direction = data.get('wind_direction')

    # Debugging the received input data
    print(f"Received Data: latitude={latitude}, longitude={longitude}, wind_speed={wind_speed}, wind_direction={wind_direction}")

    # Simulate model prediction (for testing)
    orientation = predict_orientation(latitude, longitude, wind_speed, wind_direction)

    # Debugging the prediction result
    print(f"Predicted Orientation: {orientation}")

    return jsonify({"orientation": orientation})

def predict_orientation(latitude, longitude, wind_speed, wind_direction):
    # Placeholder prediction logic for testing
    base_orientation = wind_direction + (wind_speed * 0.1)
    base_orientation = base_orientation % 360
    adjusted_orientation = base_orientation + (latitude / 100)
    adjusted_orientation = adjusted_orientation % 360
    
    return round(adjusted_orientation, 2)

if __name__ == '__main__':
    app.run(debug=True)
