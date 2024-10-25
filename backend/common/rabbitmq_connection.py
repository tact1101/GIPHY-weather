import abc
import time
import pika

SERVER_NAME = "rabbitmq_weather_to_gif_app"


class RPCConnectionInterface(abc.ABC):
    
    @abc.abstractmethod
    def connect(self, server_name) -> pika.BlockingConnection:
        """
        This method is used to create a single shared connection between microservices.
        Args:
            str: server_name
        Returns:
            pika.BlockingConnection: RabbitMQ established connection ready for use.
        """
        raise NotImplementedError("'connect' method must be implemented.")
    
    @abc.abstractmethod
    def disconnect(self) -> None:
        """
        Responsible for closing connection.
        """
        raise NotImplementedError("'disconnect' method must be implemented.")
    
class RabbitMQConnection(RPCConnectionInterface):
    """
    This class is responsible for creating a connection which will be shared among services, implenting SingleTone pattern.
    """
    _inst = None
    
    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.connection = cls._inst.connect()
        return cls._inst
    
    def __init__(self, server_name=SERVER_NAME) -> None:
        self.server_name = server_name
        self.connection = None
    
    def connect(self, server_name=SERVER_NAME):
        self.server_name = server_name 
        self.connection = None
        while not self.connection:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.server_name)) 
                # self.connection = pika.BlockingConnection(
                #     pika.ConnectionParameters(host='localhost')) 
                print("Connected to RabbbitMQ")
            except pika.exceptions.AMQPConnectionError:
                print("Waiting for RabbbitMq...")
                time.sleep(5)
        return self.connection
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print(f"Disconnected from RabbitMQ {self.server_name}")
