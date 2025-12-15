import datetime as dt
import requests
import boto3
import json
import os


# Constants
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
DEFAULT_CITIES = ['Kolkata', 'Bangalore', 'Mumbai', 'Pune', 'Hyderabad']
BUCKET_NAME = 'demobucketfordemoproject01'

def fetch_weather_data(city):
    """Fetch weather data for a given city from OpenWeatherMap API."""
    url = f"{BASE_URL}appid={API_KEY}&q={city}"
    response = requests.get(url).json()
    return response

def process_weather_response(city, response):
    """Process the API response and return formatted weather data."""
    if response.get('main'):
        now = dt.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        temp = response['main'].get('temp')
        humidity = response['main'].get('humidity')
        weather = response['weather'][0].get('description')
        wind_speed = response['wind'].get('speed')

        return {
            "city": city,
            "temperature": temp,
            "humidity": humidity,
            "weather": weather,
            "wind_speed": wind_speed,
            "timestamp": timestamp
        }
    else:
        return {
            "city": city,
            "error": "Unable to fetch weather data"
        }

def upload_to_s3(data, timestamp):
    """Upload JSON data to the specified S3 bucket."""
    client = boto3.client('s3')
    key = f'dailyreport/weather_data_{timestamp}.json'
    response = client.put_object(
        Body=json.dumps(data),
        Bucket=BUCKET_NAME,
        Key=key
    )
    return response

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    cities = event.get('Cities', DEFAULT_CITIES)
    weather_data = []
    timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    for city in cities:
        response = fetch_weather_data(city)
        data = process_weather_response(city, response)
        weather_data.append(data)

    upload_to_s3(weather_data, timestamp)

    return {
        'statusCode': 200,
        'body': f'Successfully stored weather data for cities: {[city for city in cities]}'
    }
