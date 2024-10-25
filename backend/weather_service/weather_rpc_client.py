from common import rpc, rabbitmq_connection

class WeatherRPCClient(rpc.BaseRPCClient):
    def __init__(self, connection: rabbitmq_connection.RabbitMQConnection) -> None:
        super().__init__(connection)
    
    def request_weather(self, city: str):
        """
        Args:
            WeatherService_request: 
                service_name (str): The name of the weather service to fetch the forecast from.
                city (str): The city for which to get the forecast (default is None).
        Returns:
            dict: Formatted weather forecast or an error message. 
            {"service": service_name, "city": city, "forecast": formatted_data}

        """
        request_data = {"city": city}
        self.send_request(request_data, "weather_rpc_queue")    

