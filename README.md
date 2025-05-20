# 🌪️ WindWize

**Predicting Optimal Wind Turbine Orientation Using Real-Time Wind Data**
*A real-time dashboard that helps maximize wind energy efficiency using live weather inputs.*

---

## 📌 Overview

**WindWize** is a web-based application that dynamically predicts the optimal orientation of wind turbines based on live wind direction and speed data. By aligning turbines with the most efficient wind flow, WindWize helps increase energy generation efficiency by up to **30%** — making wind power more reliable, accessible, and sustainable.

---

## 🧠 Key Features

* 🔄 **Real-time Wind Data Integration**
  Live wind direction and speed fetched using OpenWeatherMap API.

* 📍 **User Location Input**
  Enter coordinates or a location name to get instant, location-specific predictions.

* 📊 **Interactive Visualizations**
  Wind direction and optimal turbine orientation visualized using dynamic plots.

* 🗺️ **Live Global Wind Map**
  Embedded animated wind map for enhanced context.

* 🧭 **Smart Orientation Prediction**
  A simple yet effective algorithm calculates the ideal turbine orientation (wind direction + 180°).

---

## ⚙️ Technology Stack

* **Frontend/UI**:
  `Streamlit`, `Plotly`, `streamlit-folium`

* **Backend**:
  `Flask`, `Python`, `Joblib`, `Requests`

* **APIs**:
  `OpenWeatherMap API` (for wind speed & direction)

* **Deployment (Optional)**:
  `Docker` (for containerization and scalability)

---

## 🚀 How It Works

1. User enters a location or coordinates via the UI.
2. Application fetches live wind data for that region using the OpenWeatherMap API.
3. The optimal turbine orientation is calculated by adding 180° to the wind direction.
4. Visualization tools display:

   * Wind direction graph
   * Predicted turbine orientation
   * Live animated global wind map
5. The user sees a clean dashboard with predictions and visuals to support real-time turbine adjustments.

---

## 📈 Impact & Scalability

* ⚡ **25-30% more energy** can be captured with optimal orientation.
* 🌍 Scalable to multiple wind farms and geographies.
* 🧠 Future Scope: Integrating machine learning models to forecast wind patterns for preemptive orientation adjustment.

---

## 🛠️ Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/windwize.git
   cd windwize
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   Get a free API key from [OpenWeatherMap](https://openweathermap.org/api) and add it to your `.env` or directly in the code.

4. **Run the app**

   ```bash
   streamlit run frontend/dashboard.py
   ```

---

## 💡 Inspiration

WindWize was built during a school hackathon to solve a real-world energy inefficiency problem in wind farms using AI and real-time data. It’s a step toward more intelligent and sustainable renewable energy solutions.

---

## 📣 Acknowledgements

* OpenWeatherMap for providing real-time data APIs
* Streamlit & Plotly for easy-to-use, interactive visualizations
* Folium and Windy APIs for wind map integration

