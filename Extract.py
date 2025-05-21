import pandas as pd # type: ignore
import requests # type: ignore
import os
from snowflake.sqlalchemy import URL


from helpers import API_KEY, BASE_URL
from helpers import log_error

def read_city_data(file_path):
    """Read the csv file containing lat/lon city data."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        log_error(f"Failed to read file {file_path}: {e}")
        return pd.DataFrame()

def build_weather_url(lat, lon):
    """Builds a full API request URL using lat/lon."""
    return f'{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}'

def fetch_weather_data(lat, lon):
    """Sends request to OpenWeatherMap API."""
    try:
        response = requests.get(build_weather_url(lat, lon))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        log_error(f"API request failed for ({lat}, {lon}): {e}")
        return None
