from datetime import datetime


API_KEY = '6b9effe684bfcde6864f4da66277cede'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
file_path = 'API_WORK_FILES_cities.xlsx'
OUTPUT_FILE = 'weather_output.xlsx'
ERROR_LOG_FILE = 'weather_errors.log'

def log_error(message):
    """Append error messages to log file with a timestamp."""
    with open(ERROR_LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()} - {message}\n")

def kelvin_to_celsius(temp_k):
    """Convert temperature from Kelvin to Celsius."""
    return round(temp_k - 273.15, 2) if temp_k else None