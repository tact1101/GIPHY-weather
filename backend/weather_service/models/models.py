from pydantic import BaseModel

class WeatherRequestModel(BaseModel):
    city: str

class WeatherResponseModel(BaseModel):
    city: str
    forecast: str