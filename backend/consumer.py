import threading
from common import rabbitmq_connection 
from weather_service import weather_rpc_server
from gif_service.gif_rpc_server import GIFRPCServer
import logging

def start_weather_consumer(connection):
    weather_server = weather_rpc_server.WeatherServer(connection)
    weather_server.consume_tasks()

def start_gif_consumer(connection):
    gif_rpc_server = GIFRPCServer(connection)
    gif_rpc_server.consume_tasks()

if __name__ == "__main__":
    connection = rabbitmq_connection.RabbitMQConnection()
    logging.info(f"Connection has been made successfully {connection}")

    # Start both consumers in separate threads
    weather_thread = threading.Thread(target=start_weather_consumer, args=(connection,))
    gif_thread = threading.Thread(target=start_gif_consumer, args=(connection,))

    weather_thread.start()
    gif_thread.start()

    weather_thread.join()
    gif_thread.join()