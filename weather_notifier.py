import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Access variables using os.getenv()
openWeather_api_key = os.getenv("API_KEY")
weather_api_url = "https://api.openweathermap.org/data/2.5/forecast"
to_celsius = 273.15

def get_user_region():
    try:
        # Get user's IP address
        ip_info_response = requests.get('http://ip-api.com/json/')
        ip_info = ip_info_response.json()

        # return regionName
        return ip_info['regionName']

    except Exception as e:
        print(f"Error getting user IP: {e}")
        return None

def get_weather_data(region):
    try:
        # Make a request to the OpenWeatherMap API
        params = {'q': region, 'appid': openWeather_api_key}
        response = requests.get(weather_api_url, params=params)

        print("Status: ", response.status_code)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:

            print("Fetching weather data")
            # Parse the JSON content of the response
            weather_dat = response.json()

            weather_data = to_sa_format(weather_dat)

            # Do something with the parsed JSON data
            # For example, save it to a file
            with open('weather_data.json', 'w') as f:
                json.dump(weather_data, f, indent=4)
            print("Your data is ready! check weather_data.json")
        else:
            print(f"Failed to fetch weather data. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error fetching weather data: {e}")


def to_sa_format(response_json):
    list_data = response_json['list']

    for data in list_data:
        main_data = data['main']

        # Convert temperature values from Kelvin to Celsius and remove decimals
        main_data['temp'] = round(main_data['temp'] - 273.15, 1)
        main_data['feels_like'] = round(main_data['feels_like'] - 273.15, 1)
        main_data['temp_min'] = round(main_data['temp_min'] - 273.15, 1)
        main_data['temp_max'] = round(main_data['temp_max'] - 273.15, 1)

    return response_json


if __name__ == "__main__":
    region = get_user_region()

    if region:
        # if region is not None, get weather for the region
        get_weather_data(region)
