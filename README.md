# 🌦 Weather Pipeline Project

This project is a modular ETL pipeline that fetches real-time weather data using the OpenWeatherMap API, based on city coordinates (latitude and longitude) provided in an Excel file.

## 📂 Project Structure

```
weather_pipeline/
├── config.py         # API keys and constants
├── extract.py        # Data extraction (API and input file)
├── transform.py      # Data transformation/cleaning
├── load.py           # Load to DataFrame and save to Excel
├── utils.py          # Helpers like error logging, temperature conversion
├── main.py           # Orchestrates the full ETL process
```

## ✅ Requirements

- Python 3.7+
- pandas
- requests
- openpyxl

Install via:

```bash
pip install pandas requests openpyxl
```

## 🚀 How to Run

1. Put your input file named `API_WORK_FILES_cities.xlsx` in the root directory.
2. Run:

```bash
python weather_pipeline/main.py
```

3. Output will be saved as `weather_output.xlsx`.

## 📝 Input Format

The Excel file must contain columns:

- `latitude`
- `longitude`

## 🧾 Output

An Excel file with columns:

- location
- weather
- description
- temperature (°C)
- pressure
- humidity
- wind_speed
- datetime_utc
- timezone_offset_sec

## 📒 Logging

Errors are logged in `weather_errors.log`.

## 🔐 Note

Your API key is stored in `config.py`. Be cautious when pushing this to public repositories.
