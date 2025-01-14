import requests  # For making API calls
import json  # For handling JSON data
from datetime import datetime, timedelta  # For date and time manipulation
from langchain.tools import Tool  # For defining the weather_tool
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize Amadeus Client
# amadeus = Client(
#     client_id=os.getenv('AMADEUS_KEY'),
#     client_secret=os.getenv('AMADEUS_SECRET')
# )
#print(os.getenv('AMADEUS_SECRET'))

# Initialize LLM


def fetch_historical_temperature(lat: float, lon: float, date: datetime) -> float:
    """
    Fetch historical temperature for a specific date and location using the OpenWeather /3.0/onecall/timemachine endpoint.
    """
    base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    params = {
        "lat": lat,
        "lon": lon,
        "dt": int(date.timestamp()),  # Convert datetime to UNIX timestamp
        "appid": os.getenv('OPENWEATHER_API_KEY'),
        "units": "metric"  # Use metric units (Celsius)
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data["data"][0]["temp"]  # Adjust the JSON path to fetch temperature
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data: {e}")
        return None
    except KeyError:
        print("Temperature data not found in the response.")
        return None

def get_city_coordinates(city: str) -> tuple:
    """
    Fetch latitude and longitude for a city using the OpenWeather API.
    """
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": 1,
        "appid": os.getenv('OPENWEATHER_API_KEY')
    }

    response = requests.get(geo_url, params=params)
    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        return data["lat"], data["lon"]
    else:
        print(f"Error fetching coordinates for {city}: {response.status_code} - {response.text}")
        return None, None

def weather_data_fetcher(inputs):
    """
    Fetches average temperature over the last 2 years for a location identified by IATA code
    from a specific target date. Expects a dictionary input with keys 'iata_code' and 'target_date'.
    """
    print(f"Type of inputs at start: {type(inputs)}")
    print(f"Value of inputs at start: {inputs}")
    ...
    if isinstance(inputs,dict):
        pass
    else:
        try:
            inputs = json.loads(inputs)
        except json.JSONDecodeError:
            return "Error: Input must be a valid JSON string."
    
    # Extract required fields
    iata_code = inputs.get("iata_code")
    target_date = inputs.get("target_date")
    # Validate target_date format
    try:
        target_date = datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        return f"Error: Invalid date format for target_date: {target_date}. Please use YYYY-MM-DD format."

    # Simulate fetching coordinates from IATA code
    lat, lon = get_city_coordinates(iata_code)
    if not lat or not lon:
        return f"Error: Unable to fetch coordinates for IATA code {iata_code}."

    # Fetch historical temperatures
    temperatures = []
    for year_offset in range(1, 3):  # Last 2 years relative to target_date
        historical_date = target_date - timedelta(days=365 * year_offset)
        temp = fetch_historical_temperature(lat, lon, historical_date)
        if temp is not None:
            temperatures.append(temp)

    if temperatures:
        avg_temp = sum(temperatures) / len(temperatures)
        return f"The average temperature at {iata_code} over the last 2 years from {target_date.strftime('%Y-%m-%d')} is {avg_temp:.2f}°C."
    else:
        return f"Error: Unable to fetch historical weather data for {iata_code}."
    

weather_tool = Tool(
    name="Weather Fetcher",
    func=weather_data_fetcher,
    description=(
        "Fetch historical weather data for a location identified by IATA code "
        "(e.g., MAD for Madrid) and a specific target date (YYYY-MM-DD). "
        "Input must be a JSON string with keys 'iata_code' and 'target_date'."
    )
)