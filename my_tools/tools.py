from agents import function_tool
import requests

from assig4 import WEATHER_API_KEY

@function_tool
def add_numbers(a: int, b: int):
    result = a + b
    print("add_numbers function called")
    return result       

@function_tool
def get_weather(city: str) -> str:
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        print("get_weather function called")
        return f"It's {temp}°C and {condition} in {city}."
    
    return "Error fetching weather data."
@function_tool
def subtract(a: int, b: int) -> int:
    result = a - b
    print("subtract function called")
    return result

@function_tool
def multiply(a: int, b: int) -> int:
    result = a * b
    print("multiply function called")
    return result

from typing import Union

@function_tool
def divide(a: int, b: int) -> Union[float, str]:
    if b == 0:
        print("divide function called with zero divisor")
        return "Error: Division by zero is not allowed."
    result = a / b
    print("divide function called")
    return result