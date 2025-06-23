import os
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
EMAIL = os.getenv("EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")
RECIPIENT = os.getenv("RECIPIENT")

LOCATION = "Gurugram Candor Tech Space"
CITY = "Gurgaon"
COUNTRY = "IN"
LAT = 28.4595
LON = 77.0266

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
    lines.append(f"Cloud Cover: {weather['cloud_cover']}%")
    lines.append(f"Visibility: {weather['visibility']} km")
    lines.append(f"Chance of Rain: {weather['chance_of_rain']} mm")
    lines.append(f"Sunrise: {weather['sunrise']}")
    lines.append(f"Sunset: {weather['sunset']} \n")

    lines.append("🌫️ Air Quality Index (AQI)")
    lines.append(f"AQI: {aqi['aqi']} – {aqi['category']}")
    lines.append(f"PM2.5: {aqi['pm25']} µg/m³")
    lines.append(f"PM10: {aqi['pm10']} µg/m³")
    lines.append(f"CO: {aqi['co']} µg/m³")
    lines.append(f"NO₂: {aqi['no2']} µg/m³")
    lines.append(f"SO₂: {aqi['so2']} µg/m³")
    lines.append(f"O₃: {aqi['o3']} µg/m³ \n")

    lines.append("🌞 UV Index")
    lines.append(f"UV Index: {uv['value']} – {uv['category']} ({uv['note']}) \n")

    lines.append("⚠️ Concerning Parameters")
    for note in data['concerning']:
        lines.append(note)

    return "\n".join(lines)

def get_weather_data():
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_KEY}&q={CITY},{COUNTRY}&days=1&aqi=yes&alerts=no"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    current = data['current']
    forecast_day = data['forecast']['forecastday'][0]['astro']

    weather = {
        "condition": current['condition']['text'],
        "temp_c": current['temp_c'],
        "temp_f": current['temp_f'],
        "feels_like_c": current['feelslike_c'],
        "humidity": current['humidity'],
        "wind_kmh": current['wind_kph'],
        "cloud_cover": current['cloud'],
        "visibility": current['vis_km'],
        "chance_of_rain": current['precip_mm'],
        "sunrise": forecast_day['sunrise'],
        "sunset": forecast_day['sunset']
    }
    return weather

def get_air_quality_data():
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={CITY},{COUNTRY}&aqi=yes"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    air_quality = data['current']['air_quality']

    def aqi_category(pm25):
        if pm25 <= 30:
            return "Good"
        elif pm25 <= 60:
            return "Moderate"
        elif pm25 <= 90:
            return "Poor"
        elif pm25 <= 120:
            return "Very Poor"
        else:
            return "Hazardous"

    aqi = {
        "aqi": round(air_quality['pm2_5']),
        "category": aqi_category(air_quality['pm2_5']),
        "pm25": round(air_quality['pm2_5'], 1),
        "pm10": round(air_quality['pm10'], 1),
        "co": round(air_quality['co'], 1),
        "no2": round(air_quality['no2'], 1),
        "so2": round(air_quality['so2'], 1),
        "o3": round(air_quality['o3'], 1)
    }
    return aqi

def get_uv_index():
    uv = {
        "value": 0,
        "category": "Low",
        "note": "early morning reading; expected to rise during the day"
    }
    return uv

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, EMAIL_PASS)
        server.sendmail(EMAIL, to_email, msg.as_string())

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
    send_email(subject, email_body, RECIPIENT)
    print("Email sent successfully!")

if __name__ == "__main__":
    main()