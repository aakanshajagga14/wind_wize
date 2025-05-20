import streamlit as st
import plotly.graph_objects as go
import requests
import random
import time
import streamlit.components.v1 as components

API_KEY = "7beae662d05b058f7bbb2c379d8cc9dd"  

if not API_KEY:
    st.error("⚠️ API Key missing! Set it as an environment variable.")
    st.stop()

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
    return None, None 

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
    return None, None  

def plot_wind_direction_animation(wind_direction, wind_speed):
    """Create an animated plot for wind direction and wind speed."""
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[0, wind_speed],  
        theta=[0, wind_direction], 
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


st.image('https://www.trelleborg.com/marine-and-infrastructure/-/media/marine-systems/applications-and-markets/headers/infrastructure/wind_turbine_banner.jpg?h=521&iar=0&w=1916&rev=2a30ff8ea5434fa781c0ec4830e9395e&hash=781A451A8522EB1DEA0F78C5F84FF8DC', use_column_width=True)

st.title("WindWize - Dynamic Turbine Orientation Dashboard")
st.markdown("### Live Wind Map:")

wind_map_url = "https://openweathermap.org/weathermap?basemap=map&cities=true&layer=wind&zoom=3"
components.iframe(wind_map_url, height=250, width=700)  
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### Choose Input Method:")

input_method = st.radio("", ["Enter Location", "Enter Coordinates"])

latitude, longitude = None, None
wind_speed, wind_direction = None, None
orientation = None 


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
            
          
            st.subheader("Wind Direction Visualization")
            chart_placeholder = st.empty() 
            
          
            for _ in range(10): 
                if wind_speed and wind_direction:
                    fig = plot_wind_direction_animation(wind_direction, wind_speed)
                    chart_placeholder.plotly_chart(fig)
                time.sleep(1)  

            with st.spinner('Predicting Optimal Turbine Orientation...'):
                time.sleep(2) 
               
                orientation = (wind_direction + 180) % 360  
    

            if orientation is not None:
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns([1,2]) 

                with col1:
                    st.write("")  
                    st.subheader("Optimal Turbine Orientation")
                    st.markdown(f"<h2 style='color: #FF6347; font-size: 36px;'>🌀 {orientation:.2f}°</h2>", unsafe_allow_html=True)

                with col2:
                    st.write("") 
                    st.plotly_chart(fig)

elif input_method == "Enter Coordinates":
    latitude = st.number_input("🌎 Enter Latitude", format="%.6f")
    longitude = st.number_input("🌍 Enter Longitude", format="%.6f")

    if latitude and longitude:
        wind_speed, wind_direction = get_wind_data(latitude, longitude)
        if wind_speed is not None and wind_direction is not None:
            st.success(f"🌬️ Wind Speed: {wind_speed} m/s | Direction: {wind_direction}°")
        else:
            st.error("⚠️ Unable to fetch wind data. Enter manually.")
        
 
        st.subheader("Wind Direction Visualization")
        chart_placeholder = st.empty()  
        
       
        for _ in range(10): 
            if wind_speed and wind_direction:
                fig = plot_wind_direction_animation(wind_direction, wind_speed)
                chart_placeholder.plotly_chart(fig)
            time.sleep(1) 

       
        with st.spinner('Predicting Optimal Turbine Orientation...'):
            time.sleep(2)  
           
            orientation = (wind_direction + 180) % 360  
            
       
        if orientation is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1]) 

            with col1:
                st.write("") 
                st.subheader("Optimal Turbine Orientation")
                st.markdown(f"<h2 style='color: #FF6347; font-size: 36px;'>🌀 {orientation:.2f}°</h2>", unsafe_allow_html=True)

            with col2:
             
                st.write("") 
                st.plotly_chart(fig)
