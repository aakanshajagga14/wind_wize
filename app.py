import streamlit as st
import plotly.graph_objects as go
import requests
import random
import time
import streamlit.components.v1 as components

# ---------------------- Secure API Key Handling ----------------------
API_KEY = "7beae662d05b058f7bbb2c379d8cc9dd"  # Your API key directly in the code

if not API_KEY:
    st.error("⚠️ API Key missing! Set it as an environment variable.")
    st.stop()

# ---------------------- Function to Get Coordinates ----------------------
def get_coordinates(location):
    """Fetch latitude & longitude for a given location using OpenWeatherMap API."""
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}&rand={random.random()}"
    try:
        response = requests.get(geocode_url, timeout=5).json()
        if response and len(response) > 0:
            latitude = response[0]["lat"]
            longitude = response[0]["lon"]
            return latitude, longitude
    except Exception as e:
        st.error(f"Error fetching coordinates: {e}")
    return None, None  # Return None if failed

# ---------------------- Function to Get Wind Data ----------------------
def get_wind_data(latitude, longitude):
    """Fetch real-time wind speed & direction for given coordinates using OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric&rand={random.random()}"
    try:
        response = requests.get(url, timeout=5).json()
        wind_speed = response["wind"]["speed"]  # Wind speed in m/s
        wind_direction = response["wind"]["deg"]  # Wind direction in degrees
        return wind_speed, wind_direction
    except Exception as e:
        st.error(f"Error fetching wind data: {e}")
    return None, None  # Return None if failed

# ---------------------- Real-Time Animated Visualization ----------------------
def plot_wind_direction_animation(wind_direction, wind_speed):
    """Create an animated plot for wind direction and wind speed."""
    fig = go.Figure()

    # Wind direction line (animated rotation)
    fig.add_trace(go.Scatterpolar(
        r=[0, wind_speed],  # Radius is the wind speed
        theta=[0, wind_direction],  # Wind direction as the angle
        mode='lines',
        name="Wind Direction",
        line=dict(color='blue', width=4)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, 20], showticklabels=False, ticks=''),
            angularaxis=dict(showticklabels=False, ticks=''),
        ),
        showlegend=False,
        title=f"Wind Speed: {wind_speed} m/s | Direction: {wind_direction}°",
        title_x=0.5,
        title_y=0.95
    )

    return fig

# ---------------------- Streamlit UI ----------------------
# Center the UI elements and make the map thinner

# Display an image from a URL
st.image('https://www.trelleborg.com/marine-and-infrastructure/-/media/marine-systems/applications-and-markets/headers/infrastructure/wind_turbine_banner.jpg?h=521&iar=0&w=1916&rev=2a30ff8ea5434fa781c0ec4830e9395e&hash=781A451A8522EB1DEA0F78C5F84FF8DC', use_column_width=True)

st.title("WindWize - Dynamic Turbine Orientation Dashboard")
st.markdown("### Live Wind Map:")

# Embed the live wind map in the app (keep it thin and centered)
wind_map_url = "https://openweathermap.org/weathermap?basemap=map&cities=true&layer=wind&zoom=3"
components.iframe(wind_map_url, height=250, width=700)  # Thinner size for the map

# Add a padding for better spacing
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### Choose Input Method:")

input_method = st.radio("", ["Enter Location", "Enter Coordinates"])

latitude, longitude = None, None
wind_speed, wind_direction = None, None
orientation = None  # Initialize the predicted orientation variable

# 🗺️ **Option 1: Enter a Location**
if input_method == "Enter Location":
    location = st.text_input("🌍 Enter a Location (e.g., New York, London, Delhi)")
    if location:
        latitude, longitude = get_coordinates(location)
        if latitude is None or longitude is None:
            st.error("⚠️ Unable to fetch coordinates. Try again or enter manually.")
        else:
            st.success(f"📍 Location: {location} | Latitude: {latitude}, Longitude: {longitude}")

            # Fetch wind data
            wind_speed, wind_direction = get_wind_data(latitude, longitude)
            if wind_speed is not None and wind_direction is not None:
                st.success(f"🌬️ Wind Speed: {wind_speed} m/s | Direction: {wind_direction}°")
            else:
                st.error("⚠️ Unable to fetch wind data. Enter manually.")
            
            # Display the animated wind direction
            st.subheader("Wind Direction Visualization")
            chart_placeholder = st.empty()  # Placeholder for updating the graph
            
            # Simulate animation for wind direction
            for _ in range(10):  # Run for 10 seconds, update every second
                if wind_speed and wind_direction:
                    fig = plot_wind_direction_animation(wind_direction, wind_speed)
                    chart_placeholder.plotly_chart(fig)
                time.sleep(1)  # Update every second

            # Simulating prediction after animation
            with st.spinner('Predicting Optimal Turbine Orientation...'):
                time.sleep(2)  # Simulate prediction time
                # Predict the optimal turbine orientation (using a simple formula or model)
                orientation = (wind_direction + 180) % 360  # Example formula (to be replaced with actual model logic)
    
            # Display the predicted orientation on the right
            if orientation is not None:
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns([1,2])  # Two columns to align the content side by side

                with col1:
                    st.write("")  # Empty space for alignment
                    st.subheader("Optimal Turbine Orientation")
                    st.markdown(f"<h2 style='color: #FF6347; font-size: 36px;'>🌀 {orientation:.2f}°</h2>", unsafe_allow_html=True)

                with col2:
                    # Wind direction chart
                    st.write("")  # Empty space for alignment
                    st.plotly_chart(fig)

# 🌎 **Option 2: Enter Coordinates**
elif input_method == "Enter Coordinates":
    latitude = st.number_input("🌎 Enter Latitude", format="%.6f")
    longitude = st.number_input("🌍 Enter Longitude", format="%.6f")

    if latitude and longitude:
        wind_speed, wind_direction = get_wind_data(latitude, longitude)
        if wind_speed is not None and wind_direction is not None:
            st.success(f"🌬️ Wind Speed: {wind_speed} m/s | Direction: {wind_direction}°")
        else:
            st.error("⚠️ Unable to fetch wind data. Enter manually.")
        
        # Display the animated wind direction
        st.subheader("Wind Direction Visualization")
        chart_placeholder = st.empty()  # Placeholder for updating the graph
        
        # Simulate animation for wind direction
        for _ in range(10):  # Run for 10 seconds, update every second
            if wind_speed and wind_direction:
                fig = plot_wind_direction_animation(wind_direction, wind_speed)
                chart_placeholder.plotly_chart(fig)
            time.sleep(1)  # Update every second

        # Simulating prediction after animation
        with st.spinner('Predicting Optimal Turbine Orientation...'):
            time.sleep(2)  # Simulate prediction time
            # Predict the optimal turbine orientation (using a simple formula or model)
            orientation = (wind_direction + 180) % 360  # Example formula (to be replaced with actual model logic)

        # Display the predicted orientation on the right
        if orientation is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])  # Two columns to align the content side by side

            with col1:
                st.write("")  # Empty space for alignment
                st.subheader("Optimal Turbine Orientation")
                st.markdown(f"<h2 style='color: #FF6347; font-size: 36px;'>🌀 {orientation:.2f}°</h2>", unsafe_allow_html=True)

            with col2:
                # Wind direction chart
                st.write("")  # Empty space for alignment
                st.plotly_chart(fig)