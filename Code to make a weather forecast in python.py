!pip install requests
import requests
from datetime import datetime, timedelta

print("\n\n\n\n\n\t\tWelcome to the Weather Forecaster!\n\n")
print("Just Enter the City you want the weather report for\n\n")

city_name = input("Enter the name of the City: ")
forecast_date_str = input("Enter the date for weather forecast (YYYY-MM-DD) type one date ahead of the date of forecaast u want, or leave blank for current weather): ")

# Function to Get Weather Information
def get_weather(city, forecast_date=None):
    api_key = '055df2a9fb2e2305be1bf468a514196d'
    base_url_forecast = 'http://api.openweathermap.org/data/2.5/forecast'
    base_url_current = 'http://api.openweathermap.org/data/2.5/weather'

    # Get weather data based on user input (current or forecast)
    if forecast_date:
        days_until_forecast = (forecast_date - datetime.now()).days
        params_forecast = {'q': city, 'appid': api_key, 'cnt': days_until_forecast * 8}  # Adjust cnt for multiple days
        #days_until_forecast calculates the number of days between the current date and the specified forecast date.
        #cnt is the parameter used by OpenWeatherMap to specify the number of forecasts. By multiplying days_until_forecast by 8, you are effectively requesting forecasts for each 3-hour interval for the specified number of days.
        response_forecast = requests.get(base_url_forecast, params=params_forecast)
        weather_data = response_forecast.json()
        #If forecast_date is provided (i.e., it is not None), the code enters the if block and calculates the number of days until the specified forecast date using (forecast_date - datetime.now()).days. It then constructs the parameters (params_forecast) for the forecast API call, including the cnt parameter, which determines the number of forecast entries to retrieve. In this case, cnt is set to the number of days multiplied by 8, which corresponds to 8 forecast entries per day (every 3 hours). The API call is made, and the JSON response is stored in the weather_data variable.
    else:
        params_current = {'q': city, 'appid': api_key}
        response_current = requests.get(base_url_current, params=params_current)
        weather_data = response_current.json()
        #If forecast_date is None, meaning the user did not provide a specific forecast date, the code enters the else block. It constructs parameters (params_current) for the API call to retrieve the current weather information. The API call is made, and the JSON response is again stored in the weather_data variable.

    return weather_data

# Function to Display Weather Information
def display_weather_info(weather_data, user_choice=None):
    if 'list' in weather_data:
        # Display forecast information
        print(f"\nWeather Forecast for {forecast_date_str}:")
        for entry in weather_data.get('list', []):
          #weather_data.get('list', []): The OpenWeatherMap API response contains a 'list' key, which is a list of forecast entries. This loop iterates through each entry in the list.
            date = entry.get('dt_txt', '')
            #entry.get('dt_txt', ''): Retrieves the date and time of the forecast entry. This information is stored in the date variable.
            temperature = entry.get('main', {}).get('temp', '')
            #entry.get('main', {}).get('temp', ''): Retrieves the temperature from the 'main' key of the forecast entry. The temperature is stored in the temperature variable.
            description = entry.get('weather', [])[0].get('description', '')
            #entry.get('weather', [])[0].get('description', ''): Retrieves the weather description from the 'weather' key of the forecast entry. The description is stored in the description variable. Note that 'weather' is a list, and [0] is used to access the first element of that list.
            humidity = entry.get('main', {}).get('humidity', '')
            #entry.get('main', {}).get('humidity', ''): Retrieves the humidity from the 'main' key of the forecast entry. The humidity is stored in the humidity variable.
            wind_speed = entry.get('wind', {}).get('speed', '')
            #entry.get('wind', {}).get('speed', ''): Retrieves the wind speed from the 'wind' key of the forecast entry. The wind speed is stored in the wind_speed variable.

            if user_choice == 'temperature':
                print(f"{date}: Temperature {temperature}°C")
            elif user_choice == 'description':
                print(f"{date}: Description: {description}")
            elif user_choice == 'humidity':
                print(f"{date}: Humidity: {humidity}%")
            elif user_choice == 'wind speed':
                print(f"{date}: Wind Speed: {wind_speed} m/s")
            else:
                print(f"{date}: Temperature {temperature}°C, Description: {description}, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s")

    else:
        # Display current weather information
        print("\nCurrent Weather Information:")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Description: {weather_data['weather'][0]['description']}")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")

# Get and Display Weather Information
if forecast_date_str:
    forecast_date = datetime.strptime(forecast_date_str, "%Y-%m-%d")
else:
    forecast_date = None

while True:
    user_choice = input("\nEnter the weather information you want (temperature, description, humidity, wind speed), or 'exit' to end: ").lower()

    if user_choice == 'exit':
        break

    weather_data = get_weather(city_name, forecast_date)
    display_weather_info(weather_data, user_choice)
