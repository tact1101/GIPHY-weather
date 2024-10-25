from common import rpc, rabbitmq_connection
from weather_service import weather_req 
import asyncio

class WeatherServer(rpc.BaseRPCServer):
    def __init__(self, connection: rabbitmq_connection.RabbitMQConnection) -> None:
        super().__init__(connection, "weather_rpc_queue")
        
    async def process_data(self, request_data):
        service_name = request_data.get('service_name')
        city = request_data.get('city')
        loop = asyncio.get_event_loop() # create an event loop
        weather_data = await loop.run_in_executor(weather_req.weather_service_handler.fetch_forecast(service_name, city))  
        # Fetch weather data for the city warpping sync function in in an async call with thread pool 
        return weather_data
