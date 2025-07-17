# automated-weather-report-generator
# 📬 Daily Weather & AQI Email Bot

Automatically sends you a daily weather and air quality report by email every morning at **8:00 AM IST**.

Perfect for:
- Tracking your local **weather, temperature, AQI, sunrise/sunset** daily
- Learning **GitHub Actions**, Python scripting, and free cloud automation
- Showcasing a real-world automation project in your GitHub portfolio

---

## 📦 Features
- 🌤 **Current weather** (description, temp, min/max)
- 💨 **AQI** (Air Quality Index)
- 🌅 **Sunrise/Sunset** timings
- 🕗 **Scheduled daily at 8 AM IST** using GitHub Actions
- 📧 Sends a **text email** directly to your inbox

---

## 🧰 Technologies Used
- Python 3.10
- GitHub Actions (cron job)
- OpenWeatherMap API (free tier)
- SMTP (Gmail) to send email

---

## 🔧 Setup Instructions

### 1. Fork or Clone the Repo
```bash
git clone https://github.com/tharunerd/automated-weather-report-generator.git
```

### 2. Add GitHub Secrets
Go to `Settings > Secrets > Actions` in your GitHub repository and add the following secrets:

| Name                | Value Description                    |
|---------------------|--------------------------------------|
| `OPENWEATHER_API_KEY` | Get it from https://openweathermap.org/api |
| `EMAIL`              | Your Gmail address                  |
| `EMAIL_PASS`         | Gmail App Password (not regular password) |
| `RECIPIENT`          | Your recipient email address        |

📌 **Note:** For Gmail, enable 2FA and generate an **App Password** [here](https://myaccount.google.com/apppasswords)

---

## 📁 Project Structure
```text
.
├── main.py                      # Fetches data and sends email
├── .github/workflows/schedule.yml  # GitHub Actions workflow
└── .env                        # For local testing (not pushed)
```

---

## 📬 Sample Email
```
📍 Daily Weather & Air Report – Gurugram
Date: 23 June 2025 | Time: 08:00 AM IST

🌤 Weather: Partly Cloudy
🌡 Temp: 31°C (High: 34°C | Low: 27°C)
🌅 Sunrise: 05:27 AM | 🌇 Sunset: 07:19 PM

💨 AQI: 92 – Moderate
🔆 UV Index: [Not available on free tier]

Stay hydrated. Have a calm, productive day!
– AutoWeatherBot
```

![Weather Report Screenshot](C:\Users\AKULAKUM\OneDrive - Capgemini\Desktop\git projects\automated-weather-report-generator\Result_1.png)

---

## 🌍 Credits
Made with ❤️ by [Tharun Kumar Akula](https://github.com/tharunerd)

Data provided by:
- [OpenWeatherMap](https://openweathermap.org/)

---

## 📌 License
This project is licensed under the [MIT License](LICENSE).

Feel free to fork and improve! Pull requests welcome.
