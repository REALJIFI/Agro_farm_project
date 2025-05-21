from datetime import datetime
from helpers import log_error, kelvin_to_celsius


def parse_weather_data(data):
    """
    Extract relevant weather information from the API response.
    """
    try:
        location = data.get('name')
        weather = data['weather'][0].get('main')
        description = data['weather'][0].get('description')
        temperature = kelvin_to_celsius(data['main'].get('temp'))
        pressure = data['main'].get('pressure')
        humidity = data['main'].get('humidity')
        wind_speed = data['wind'].get('speed')
        dt = data.get('dt')
        timezone = data.get('timezone')

        return {
            'location': location,
            'weather': weather,
            'description': description,
            'temperature (°C)': temperature,
            'pressure': pressure,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'dt': dt,
            'timezone': timezone
        }
    except (KeyError, IndexError, TypeError) as e:
        log_error(f"Failed to parse data: {e}")
        return None

def enhance_weather_data(df):
    """
    Convert 'dt' + 'timezone' to a readable date and time format, and restructure the DataFrame.
    """
    try:
        # Create a new datetime column adjusted for timezone
        df['Reading_date'] = df.apply(
            lambda row: datetime.fromtimestamp(row['dt'] + row['timezone']), axis=1
        )

        # Drop the original UNIX datetime and timezone columns
        df.drop(['dt', 'timezone'], axis=1, inplace=True)

        # Split the datetime into separate Date and Time columns
        df['Date'], df['Time'] = zip(*[
            (d.date(), d.time()) for d in df['Reading_date']
        ])

        # Drop intermediate column to finalize structure
        df.drop(['Reading_date'], axis=1, inplace=True)

        return df
    except Exception as e:
        log_error(f"Failed to enhance dataframe with datetime info: {e}")
        return df
