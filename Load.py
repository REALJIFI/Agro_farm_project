
from sqlalchemy import create_engine 
from dotenv import load_dotenv
import os
from snowflake.sqlalchemy import URL
import pandas as pd 
from helpers import log_error



def load_to_db(df):
    """
    Load the transformed DataFrame into the database table 'WEATHER' using
    connection parameters from environment variables.
    """
    try:
        # Create the connection URL using environment variables for security
        connection_url = URL.create(
            drivername="snowflake",  
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_ACCOUNT"),  # sometimes this might be 'host' depending on DB
            database=os.getenv("DB_NAME"),
            query={
                "schema": os.getenv("DB_SCHEMA"),
                "warehouse": os.getenv("DB_WAREHOUSE")
            }
        )
        
        # Create the SQLAlchemy engine
        engine = create_engine(connection_url)

        # Load the DataFrame into the 'WEATHER' table, appending data without the index
        df.to_sql('WEATHER', con=engine, if_exists='append', index=False)
        
        print("Data loaded successfully to the database.")
        
    except Exception as e:
        log_error(f"Error loading data to DB: {e}")



def create_weather_dataframe(records):
    """Convert list of dictionaries to a DataFrame."""
    return pd.DataFrame(records)

def save_to_excel(df, file_name):
    """Save DataFrame to Excel."""
    try:
        df.to_excel(file_name, index=False)
        print(f" Weather data saved to {file_name}")
    except Exception as e:
        log_error(f"Error saving Excel: {e}")
        print(" Failed to save file. See log.")
