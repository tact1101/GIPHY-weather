import logging
from threading import Thread
from gif_service.gif_rpc_server import GIFRPCServer  # Assuming this is the correct import for your consumer
from common.rabbitmq_connection import RabbitMQConnection  # Assuming this is how you're handling RabbitMQ connection
import asyncio
from gif_service import gif_rpc_client

# Test function to run the consumer in a separate thread
def run_consumer():
    connection = RabbitMQConnection()  # Ensure your RabbitMQ connection setup works here
    server = GIFRPCServer(connection)

    # Start the consumer loop
    asyncio.run(server.consume_tasks())

if __name__ == "__main__":
    # Start the consumer in a separate thread to simulate the real consumer running in the background
    consumer_thread = Thread(target=run_consumer, daemon=True)
    consumer_thread.start()

    # Create the RPC client to send the request and get the response
    rpc_client = gif_rpc_client.GIFRPCClient(RabbitMQConnection())

    # Send a test request for the 'cats' tag and print the result
    logging.info("Sending test RPC request for 'cats'")
    response = rpc_client.request_gif(tag="cats")
    logging.info(f"Received response: {response}")