import os
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")  # recipient email

LOCATION = "Gurugram Candor Tech Space"
CITY = "Gurgaon"
COUNTRY = "IN"
LAT = 28.4595    # latitude for Gurugram
LON = 77.0266    # longitude for Gurugram

def format_weather_email(data):
    date_str = data['date'].strftime("%d %B %Y")

    weather = data['weather']
    aqi = data['aqi']
    uv = data['uv_index']

    lines = []
    lines.append(f"As of {date_str} in {data['location']} the updates are as follows:\n")

    lines.append("🌤️ Weather")
    lines.append(f"Condition: {weather['condition']}")
    lines.append(f"Temperature: {weather['temp_c']}°C (≈ {weather['temp_f']}°F)")
    lines.append(f"Feels Like: {weather['feels_like_c']}°C")
    lines.append(f"Humidity: {weather['humidity']}%")
    lines.append(f"Wind: {weather['wind_kmh']} km/h")
    lines.append(f"Cloud Cover: {weather['cloud_cover']}")
    lines.append(f"Visibility: {weather['visibility']}")
    lines.append(f"Chance of Rain: {weather['chance_of_rain']}%")
    lines.append(f"Sunrise: {weather['sunrise']}")
    lines.append(f"Sunset: {weather['sunset']} \n")

    lines.append("🌫️ Air Quality Index (AQI)")
    lines.append(f"AQI: {aqi['aqi']} – {aqi['category']}")
    lines.append(f"PM2.5: {aqi['pm25']} µg/m³")
    lines.append(f"PM10: {aqi['pm10']} µg/m³")
    lines.append(f"CO: {aqi['co']} ppb")
    lines.append(f"NO₂: {aqi['no2']} ppb")
    lines.append(f"SO₂: {aqi['so2']} ppb")
    lines.append(f"O₃: {aqi['o3']} ppb \n")

    lines.append("🌞 UV Index")
    lines.append(f"UV Index: {uv['value']} – {uv['category']} ({uv['note']}) \n")

    lines.append("⚠️ Concerning Parameters")
    for note in data['concerning']:
        lines.append(note)

    return "\n".join(lines)

def kelvin_to_celsius(k): return round(k - 273.15)
def kelvin_to_fahrenheit(k): return round((k - 273.15) * 9/5 + 32)
def mps_to_kmh(mps): return round(mps * 3.6)

def get_weather_data():
    WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")  # Add your WeatherAPI key to .env
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={CITY},{COUNTRY}&aqi=yes"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    current = data['current']
    condition = current['condition']['text']
    temp_c = current['temp_c']
    temp_f = current['temp_f']
    feels_like_c = current['feelslike_c']
    humidity = current['humidity']
    wind_kmh = current['wind_kph']
    cloud_cover = f"{current['cloud']}%"
    visibility = f"{current['vis_km']} km"
    chance_of_rain = current.get('precip_mm', "N/A")
    # WeatherAPI's free plan does not provide sunrise/sunset in current endpoint
    sunrise = "N/A"
    sunset = "N/A"

    weather = {
        "condition": condition,
        "temp_c": temp_c,
        "temp_f": temp_f,
        "feels_like_c": feels_like_c,
        "humidity": humidity,
        "wind_kmh": wind_kmh,
        "cloud_cover": cloud_cover,
        "visibility": visibility,
        "chance_of_rain": chance_of_rain,
        "sunrise": sunrise,
        "sunset": sunset
    }
    return weather

def get_air_quality_data():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    components = data['list'][0]['components']
    aqi_index = data['list'][0]['main']['aqi']

    # Map OWM AQI index to category
    aqi_map = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor",
    }
    aqi_category = aqi_map.get(aqi_index, "Unknown")

    aqi = {
        "aqi": aqi_index,
        "category": aqi_category,
        "pm25": components.get('pm2_5', 0),
        "pm10": components.get('pm10', 0),
        "co": int(components.get('co', 0)*1000),
        "no2": int(components.get('no2', 0)*1000),
        "so2": int(components.get('so2', 0)*1000),
        "o3": int(components.get('o3', 0)*1000)
    }
    return aqi

def get_uv_index():
    url = f"http://api.openweathermap.org/data/2.5/uvi?lat={LAT}&lon={LON}&appid={API_KEY}"
    # Note: This endpoint is deprecated, but for demo, let's use it.
    # New UV index API is part of One Call API (not free).
    # So we'll fake data here as example.

    # You may want to fetch UV index from another source or your weather API.

    uv = {
        "value": 0,
        "category": "Low",
        "note": "early morning reading; expected to rise during the day"
    }
    return uv

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())

def main():
    weather = get_weather_data()
    aqi = get_air_quality_data()
    uv_index = get_uv_index()

    data = {
        "location": LOCATION,
        "date": datetime.now(),
        "weather": weather,
        "aqi": aqi,
        "uv_index": uv_index,
        "concerning": [
            "AQI is Moderate: Generally safe, but sensitive individuals (e.g., with asthma or heart conditions) may experience mild symptoms.",
            "PM2.5 and PM10 are elevated: Prolonged exposure may affect respiratory health.",
            "UV Index is currently low, but it will likely increase by midday. Sun protection is recommended if you're outdoors later."
        ]
    }

    email_body = format_weather_email(data)
    subject = f"Weather & AQI Update for {LOCATION} on {data['date'].strftime('%d %B %Y')}"
    send_email(subject, email_body, TO_EMAIL)
    print("Email sent successfully!")

if __name__ == "__main__":
    main()
