import requests

# NOAA API Endpoint for Wind Data (Replace with your actual API URL)
API_URL = "https://api.weather.gov/gridpoints/LOX/154,37/forecast/hourly"

# Mapping wind directions to degrees
WIND_DIRECTIONS = {
    "N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5, "E": 90,
    "ESE": 112.5, "SE": 135, "SSE": 157.5, "S": 180,
    "SSW": 202.5, "SW": 225, "WSW": 247.5, "W": 270,
    "WNW": 292.5, "NW": 315, "NNW": 337.5
}

def fetch_wind_data():
    response = requests.get(API_URL)
    data = response.json()

    clean_data = []
    for period in data["properties"]["periods"][:5]:  # Fetch next 5 hours
        wind_speed_mph = int(period["windSpeed"].split()[0])  # Extract number
        wind_speed_mps = round(wind_speed_mph * 0.44704, 2)  # Convert mph to m/s
        wind_direction_str = period["windDirection"]
        wind_direction_deg = WIND_DIRECTIONS.get(wind_direction_str, None)  # Convert to degrees

        clean_data.append({
            "timestamp": period["startTime"],
            "temperature_C": round((period["temperature"] - 32) * 5/9, 2),  # Convert °F to °C
            "humidity_%": period["relativeHumidity"]["value"],
            "wind_speed_mps": wind_speed_mps,
            "wind_direction_deg": wind_direction_deg
        })

    return clean_data

if __name__ == "__main__":
    wind_data = fetch_wind_data()
    print(wind_data)  # Test output
