import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import FindClosest

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"
latitude = input("Please enter the latitude: ")
longitude = input("Please enter longitude: ")

params = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": ["apparent_temperature_mean", "rain_sum"],
    "timezone": "auto",
    "temperature_unit": "fahrenheit",
}

responses = openmeteo.weather_api(url, params)
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

daily = response.Daily()
daily_apparent_temperature_mean = daily.Variables(0).ValuesAsNumpy()
daily_rain_sum = daily.Variables(1).ValuesAsNumpy()

daily_data = {"date and time": pd.date_range(
    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["apparent_temperature_mean"] = daily_apparent_temperature_mean
daily_data["rain_sum"] = daily_rain_sum

daily_dataframe = pd.DataFrame(data = daily_data)
print("\nDaily data\n", daily_dataframe)

index = FindClosest.findClosest(68, daily_apparent_temperature_mean, daily_rain_sum)
if index == -1:
    print("There are no good walking days.")
else:
    print(f"The best walking day is {daily_data["date and time"].date [index]}")



