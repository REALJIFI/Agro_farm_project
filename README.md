# 🌦  Project Overview
This project builds a modular and scalable ETL (Extract, Transform, Load) pipeline to collect real-time weather data from the OpenWeatherMap API for multiple locations. The pipeline extracts relevant weather attributes such as temperature, humidity, wind speed, and weather conditions, transforms and formats the data for readability, and loads it into a Snowflake data warehouse for long-term storage, analytics, or dashboarding.
The solution is structured for clarity, modularity, and future scalability.

## Project Problem
Agricultural stakeholders and environmental analysts in regions like Nigeria often struggle to access and aggregate timely, accurate weather data from multiple geographic locations. This lack of accessible environmental data hinders effective decision-making in:

Agricultural planning and irrigation

Early warning systems for extreme weather

Climate and environmental impact assessments

Location-specific trend analysis and forecasting

Manual data collection is error-prone, slow, and not scalable.

## Recommendations
To solve these challenges, this project implements:

Automated Data Extraction:

Uses OpenWeatherMap API to fetch real-time weather data for a list of cities with pre-defined coordinates from an Excel file.

Data Transformation:

Converts Unix timestamps to human-readable formats (date and time).

Cleans and structures the data for database ingestion.

Ensures data consistency and standardization.

Cloud-Based Storage in Snowflake:

Scalable cloud warehouse ingestion using SQLAlchemy and environment variables for secure credential management.

Table creation and appending logic included for incremental loads.

Modular Codebase:

Separated into extract.py, transform.py, and load.py scripts.

Enables easy debugging, maintenance, and reuse in other projects.


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

