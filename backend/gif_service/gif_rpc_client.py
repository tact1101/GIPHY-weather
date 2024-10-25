from common import rpc, rabbitmq_connection

class GIFRPCClient(rpc.BaseRPCClient):
    def __init__(self, connection: rabbitmq_connection.RabbitMQConnection) -> None:
        super().__init__(connection)

    def request_gif(self, tag: str = None, rating: str = "pg-13") -> dict:
        """
        Args:
            tag: str = None
            rating: str = "pg-13"
        Returns:
            dict:
            {"gif_url": gif_url, "title": title}

        """
        request_data = {
            "tag": tag,
            "rating": rating,
            }
        self.send_request(request_data, "gif_rpc_queue")
