from common import rpc, rabbitmq_connection
from gif_service import giphy_req
import logging 

class GIFRPCServer(rpc.BaseRPCServer):
    def __init__(self, connection: rabbitmq_connection.RabbitMQConnection) -> None:
        super().__init__(connection, 'gif_rpc_queue')
        logging.info("GIFRPCServer is ready and listenning in gif_rpc_queue.")

    async def process_data(self, request_data):
        tag = request_data.get('tag')
        logging.info(f"Received data from queue: {request_data}")
        gif_data = await giphy_req.fetch_random_gif(tag)  # Fetch GIF based on the tag
        logging.info(f"Fetched gif: {gif_data}.")
        return gif_data