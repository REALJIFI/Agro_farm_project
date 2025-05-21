import logging
from helpers import file_path, OUTPUT_FILE
from Extract import read_city_data, fetch_weather_data
from Transform import parse_weather_data, enhance_weather_data
from Load import create_weather_dataframe, save_to_excel, load_to_db

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Extract
        logger.info("Reading city coordinates from Excel...")
        city_df = read_city_data(file_path)
        if city_df.empty:
            logger.error("No data found in city file.")
            return

        weather_records = []
        for _, row in city_df.iterrows():
            lat, lon = row['latitude'], row['longitude']
            data = fetch_weather_data(lat, lon)
            if data:
                parsed = parse_weather_data(data)
                if parsed:
                    weather_records.append(parsed)

        if not weather_records:
            logger.error("No weather data retrieved.")
            return

        # Transform
        logger.info("Transforming weather data...")
        weather_df = create_weather_dataframe(weather_records)
        weather_df = enhance_weather_data(weather_df)
        logger.info("Transformation complete.")

        # Load
        logger.info("Saving weather data to Excel...")
        save_to_excel(weather_df, OUTPUT_FILE)

        logger.info("Loading data to database...")
        load_to_db(weather_df)
        logger.info("ETL pipeline completed successfully.")

    except Exception as e:
        logger.exception(f"ETL pipeline failed: {e}")

if __name__ == "__main__":
    main()
