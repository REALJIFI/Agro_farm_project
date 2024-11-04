# importing librabries
import requests
import pandas as pd
from datetime import datetime

# load to Snowflake DB
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from snowflake.sqlalchemy import URL

# making a request( api call)
api_key = '6b9effe684bfcde6864f4da66277cede'
lon = 5.47631
lat = 7.025853
url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

response = requests.get(url)

# check your status code to be sure you got the response you expected 
# if output is 200 then you good to go
response.status_code

# view response
data = response.json()
data

location= data['name']
weather = data['weather'][0]['main']
description = data['weather'][0]['description']
temp = data['main']['temp']
pressure = data['main']['pressure']
humidity = data['main']['humidity']
speed = data['wind']['speed']
Date = data['dt']
time = data['timezone']

### next step create DataFrame with pandas
# At this stage you have extracted from Dat_awarehouse and you are building a data_pipeline( ETL)
df = pd.DataFrame([{'location': location,
                    'weather': weather,
                    'description': description,
                    'temperature': temp,
                    'pressure': pressure,
                    'humidity': humidity,
                    'speed': speed,
                    'dt': Date,
                    'timezone': time}])
df

# step 1 input the excel file into the pipeline
all_locations = pd.read_excel(R'C:\Users\back2\Desktop\DATA ENGINEERIGN FOLDER\API_AGRO FARM PROJECT\API_WORK_FILES_cities.xlsx')
all_locations.head()

#step 2:create an empty list that will retain all the relevant info or colunms that is already created.
locations = []
weathers = []
descriptions = []
temps = []
pressures = []
humidities = []
speeds = []
Dates = []
times = []

# step 3 : loop through the excel datatframe and iterate to get the data you want.

for index, row in all_locations.iterrows():
        
        api_key = '6b9effe684bfcde6864f4da66277cede'
        lon = row['longitude']
        lat = row['latitude']
        
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

        response = requests.get(url)
        data = response.json()
         
        location= data['name']
        locations.append(location)

        weather = data['weather'][0]['main']
        weathers.append(weather)

        description = data['weather'][0]['description']
        descriptions.append(description)

        temp = data['main']['temp']
        temps.append(temp)

        pressure = data['main']['pressure']
        pressures.append(pressure)

        humidity = data['main']['humidity']
        humidities.append(humidity)

        speed = data['wind']['speed']
        speeds.append(speed)

        Date = data['dt']
        Dates.append(Date)

        time = data['timezone']
        times.append(time)

#Creating my DataFrame
df = pd.DataFrame({'location': locations,
                    'weather': weathers,
                    'description': descriptions,
                    'temperature': temps,
                    'pressure': pressures,
                    'humidity': humidities,
                    'speed': speeds,
                    'dt': Dates,
                    'timezone': times})
df

### Transformation
# first of all make a copy of your dataframe to avoid tampering with the originally created one
df2 = df.copy()

# First assisgnment can be simply done this way
# convert temperature reading to celcius
# this function was only applied to a colunm
df2['temperature'].apply(lambda x: x - 273.15) 

# second assignment 
#convert date and timezone from seconds to readable format(int timezone you add or subtract)
from datetime import datetime
def adjust_date(row):
    unix_datetime = row['dt'] + row['timezone']

    #conversion
    actual_datetime = datetime.fromtimestamp(unix_datetime)
    return actual_datetime

# this function is being applied to the colunm and rows
# NB: axis zero(0) is rows while axis one(1) is columns
df2.apply(adjust_date, axis=1)

# create a new colunm called reading date
df2['Reading_date'] = df2.apply(adjust_date, axis=1)

#remove or drop dt and timezone to make table look standard
df2.drop(['dt', 'timezone'], axis=1, inplace = True)

# Split date and time in the dataframe
df2['Date'],df2['Time'] = zip(*[(d.date(), d.time()) for d in df2['Reading_date']])

# drop reading_date after the split for a clean and standard DataFrame
df2.drop(['Reading_date'], axis=1, inplace = True)

### Loading To database
engine = create_engine(URL(
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        account = os.getenv("DB_ACCOUNT"),
        database = os.getenv("DB_NAME"),
        schema = os.getenv("DB_SCHEMA"),
        warehouse = os.getenv("DB_WAREHOUSE")
))

load_dotenv(override=True)
os.getenv('password')

df2.to_sql('WEATHER', con=engine, if_exists='append',index=False)