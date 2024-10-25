from fastapi import APIRouter, HTTPException
from weather_service import weather_rpc_client
from common.rabbitmq_connection import RabbitMQConnection

router = APIRouter()

@router.get("/weather/get_forecast")
async def get_weather_forecast(service_name: str, city: str = None) -> dict:
    """
    Unified endpoint to get weahter forecasts based on the service.
    Args:
        service_name (str): The name of the weather service to fetch the forecast from.
        city (str): The city for which to get the forecast (default is None).
    
    Returns:
        Dict: Weather forecast or error message.
    """
    if not city:
        raise HTTPException(status_code=400, detail="City name must be provided.")
    try:  
        rpc_client = weather_rpc_client.WeatherRPCClient(RabbitMQConnection())      
        forecast = rpc_client.request_weather(service_name, city)
        return forecast
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error {str(e)}") 