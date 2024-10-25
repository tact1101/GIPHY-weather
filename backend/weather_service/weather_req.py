from common.api_key import WEATHER_API_KEY
from geopy.geocoders import Nominatim
import abc
import requests
import fastapi
from pydantic import BaseModel

class URLBuilder:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def construct_url(self, lat: float, lon: float) -> str:
        """Constructs a URL for API request.
        
        Args:
            lat (float): Latitude of a given city.
            lon (float): Longtitude of a given city.
        Returns:
            str: The url which can then be used to make a request weather service.
        """
           
class FiveDayForecastURLBuilder(URLBuilder):
    def construct_url(self, lat: float, lon: float) -> str:
        return (f"https://api.openweathermap.org/data/2.5/forecast?"
                f"lat={lat}&lon={lon}&appid={self.api_key}&units=metric")

class GeocodingService(metaclass=abc.ABCMeta):
    """
    Responsible for providing geographical coordinates (latitude and longtitude) corresponding to a location.
    """
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'get_lat_lon') and 
                callable(getattr(subclass, 'get_lat_lon')))
    
    def get_lat_lon(self, city: str) -> tuple:
        """
        Gets latitude and longtitude corresponding to a location (city).
        Args:
            city (str): requested location.
        Returns:
            tuple: (latitude, longtitude) respactive to a location (city).
        Rises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("Subclasses must implement 'get_lat_lon' method.")

class GoecodingNominatim:
    def get_lat_lon(self, city: str) -> tuple:
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(city)
        if not location:
            raise ValueError(f"City '{city}' was not found.")
        return (location.latitude, location.longitude)
        
class ForecastFormatter(metaclass=abc.ABCMeta):
    """
    Responsible for formatting the forecast API reponse.
    """
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'format_forecast') and
                callable(getattr(subclass, 'format_forecast')))
    
    def format_forecast(self, forecast: dict) -> str:
        """
        Gets latitude and longtitude corresponding to a location (city).
        Args:
            forecast (dict): response from the weather service.
        Returns:
            generator: it holds (str) formatted, easier to read weather forecast.
        Rises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("Subclasses must implement 'format_forecast' method.")

class OpenWeatherForecastFormatter:
    def format_forecast(self, forecasts):
        print(f"Total forecast entries: {len(forecasts)}")  # Should be 40 for 5 days
        for forecast in forecasts:
            dt_txt = forecast['dt_txt']  # Date and time of the forecast
            temp = forecast['main']['temp']  # Temperature
            weather_desc = forecast['weather'][0]['description']  # Weather description
            feels_like = forecast['main']['feels_like']
            min_max_temp = f"{forecast['main']['temp_min']}°C to {forecast['main']['temp_max']}°C"
            humidity = forecast['main']['humidity']
            
            yield (f"On {dt_txt}, the temperature will be {temp}°C, with {weather_desc}. "
                   f"It will feel like {feels_like}°C. The temperature range will be between {min_max_temp}, "
                   f"and the humidity will be {humidity}%.")
    
    def weather_details(self):
        pass

class WeatherService(metaclass=abc.ABCMeta):
    """
    Responsible for making a request to weather API and handling it's responses.
    """
    @classmethod
    def __subclasshook__(csl, subclass: type) -> bool:
        return (hasattr(subclass, 'req_forecast') and
                callable(getattr(subclass, "req_forecast")))
    
    def req_forecast(self, city: str) -> dict:
        """
        Request the weather forecast for a given city.

        Args:
            city (str): The name of the city for which to request the forecast.
        
        Returns:
            dict: The weather forecast data in JSON format or another appropriate format.
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("Subclasses must implement 'req_forecast' method.")
        

class FiveDayForecastOpenWeatherAPI:
    def __init__(self, geocoding_service: GeocodingService, url_builder: URLBuilder) -> None:
        self.url_builder= url_builder
        self.geocoding_service = geocoding_service
        
    def req_forecast(self, city: str):
        lat, lon = self.geocoding_service.get_lat_lon(city)   
        url = self.url_builder.construct_url(lat, lon)
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['list']  # List of 5-day forecasts (each in 3-hour intervals)
        except requests.exceptions.HTTPErrorP as e:
            return str(e)

class UnifiedWeatherServiceHandler:
    
    def __init__(self, services: dict) -> None:
        """
        Initialize the handler with multiple weather services and their corresponding formatters.

        Args:
            services (Dict[WeatherService, ForecastFormatter]): A dictionary that maps a weather service to its formatter.
        """
        self.services = services
    
    def fetch_forecast(self, service_name: str, city: str) -> dict:
        """
        Fetch forecasts from a weather service and format them.

        Args:
        service_name (str): The name of the service to fetch the weather from.
        city (str): The city for which to fetch the weather forecast.

        Returns:
        dict: Formatted weather forecast or an error message. 
        {"service": service_name, "city": city, "forecast": formatted_data}
        """
        # Find the correct weather service and formatter
        try:
            for service, formatter in self.services.items():
                if service.__class__.__name__ == service_name and isinstance(service, WeatherService):
                    forecast_data = service.req_forecast(city)
                    if not forecast_data:
                        raise ValueError(f"No forecast data found for city: {city}")
                    formatted_data = list(formatter.format_forecast(forecast_data))
                    return {"service": service_name, "city": city, "forecast": formatted_data}
            
            raise NameError(f"Weather service '{service_name}' not found.")

        except requests.exceptions.RequestException as e:
            raise fastapi.HTTPException(status_code=502, detail=f"Failed to connect to the weather service: {str(e)}")
        except ValueError as e:
            raise fastapi.HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise fastapi.HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



# Create geocoding service 
geocoding_service = GoecodingNominatim()   

# Create a URL builder and OpenWeatherAPI service 
five_day_url_builder = FiveDayForecastURLBuilder(api_key=WEATHER_API_KEY)
open_weather_api = FiveDayForecastOpenWeatherAPI(geocoding_service, five_day_url_builder) 

# Create a forecast formatter to output forecasts
forecast_formatter = OpenWeatherForecastFormatter()

# Initialize the MultiWeatherServiceHandler
weather_service_handler = UnifiedWeatherServiceHandler(
    {
        open_weather_api: forecast_formatter,
        # Add other services and formatters here
    }
)

# forecast = open_weather_api.req_forecast('London')   
# for formatted in forecast_formatter.format_forecast(forecast):
#     print(formatted)
