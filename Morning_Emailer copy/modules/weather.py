import requests
import os

class Weather:
    def __init__(self, city, country):
        self.api_key =  os.getenv("WEATHER_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"

    def obtain_weather_url(self, country, city):
        """
        Constructs the URL for the API call and retrieves weather data.
        """
        url = f"{self.base_url}appid={self.api_key}&q={city},{country}"
        response = requests.get(url).json()
        return response

    @staticmethod
    def kelvin_to_celsius_fahrenheit(kelvin):
        """
        Converts temperature from Kelvin to Celsius and Fahrenheit.
        """
        celsius = kelvin - 273.15
        fahrenheit = celsius * (9/5) + 32
        return celsius, fahrenheit

    def get_temp_celsius_fahrenheit(self, country, city):
        """
        Gets the temperature in Celsius and Fahrenheit for a specified location.
        """
        weather_data = self.obtain_weather_url(country, city)
        temp_kelvin = weather_data['main']['temp']
        temp_celsius, temp_fahrenheit = self.kelvin_to_celsius_fahrenheit(temp_kelvin)
        return temp_celsius, temp_fahrenheit
    
    def obtain_weather_description(self, country, city):
        weather_data = self.obtain_weather_url(country, city)
        weather_description = weather_data['weather'][0]['description']
        return weather_description
    
    def get_message(self, country, city):
        """
        Provides a detailed weather description with temperature, condition,
        clothing suggestion, and additional recommendation based on rain or snow.
        """
        # Obtain weather data and temperature
        weather_data = self.obtain_weather_url(country, city)
        temp_kelvin = weather_data['main']['temp']
        temp_celsius, _ = self.kelvin_to_celsius_fahrenheit(temp_kelvin)

        # Obtain weather condition
        weather_description = weather_data['weather'][0]['description']
        
        # Initial message with temperature and description
        message = f"It is currently {temp_celsius:.1f}°C outside and there is {weather_description}."

        # Clothing suggestion based on temperature
        if temp_celsius > 25:
            message += " It is suggested that you wear light clothing, such as shorts and a shirt."
        elif 18 <= temp_celsius <= 25:
            message += " It is suggested that you wear light clothing, such as pants and a t-shirt."
        elif 10 <= temp_celsius < 18:
            message += " It is suggested that you wear warmer clothing, such as pants and a hoodie."
        else:
            message += " It is suggested that you wear warm clothing, such as pants and a jacket."

        # Additional recommendation based on weather conditions
        if 'rain' in weather_description.lower():
            message += " You should also consider adding a raincoat due to the rain."
        elif 'snow' in weather_description.lower():
            message += " You should also consider adding snowpants due to the snowa."

        return message