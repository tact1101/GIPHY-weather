import json
# from fastapi import FastAPI
# import asyncio
# import pika
# from rabbitmq_connection import RabbitMQConnection


# class BaseRPCServer:
#     """
#         Initializes the RPCServer instance. Subclasses must implement async method 'process_data'.

#         Args:
#             connection (RabbitMQConnection): An instance of RabbitMQConnection used to connect to RabbitMQ.
#     """
#     def __init__(self, connection: RabbitMQConnection, queue_name: str) -> None:
#         self.connection = connection.connect()
#         self.channel = self.connection.channel()
#         self.channel.queue_declare(queue=queue_name)  # "gif_rpc_queue"
#         self.channel.basic_qos(prefetch_count=1)
#         self.queue_name = queue_name
    
#     async def __on_request(self, ch, method, props, body):
#         """
#         Callback method to handle incoming requests.

#         Args:
#             ch: The channel object.
#             method: The method frame that contains delivery info.
#             props: The properties of the message.
#             body: The message body containing request data.
#             request_data (dict): The data to request. 
            
#         """
#         # i dont' want in props a fethcer which is a function i need to be run right away, 
#         # since it has to be awaited and the data which is awaited must be stored
#         request_data = json.loads(body) # parse incoming data
#         try:
#             data = await self.process_data(request_data)
#             response_body = json.dumps(data)
#             ch.basic_publish(
#                 exchange='',
#                 routing_key=props.reply_to,
#                 body=response_body,
#                 properties=pika.BasicProperties(
#                     correlation_id=props.correlation_id
#                 )
#             )
#             print(f"Fetched data: {data}")
#         except Exception as e:
#             print(f"Error fetching data: {e}")
#         finally:
#             # Acknowledge the message
#             ch.basic_ack(delivery_tag=method.delivery_tag)
            
#     def consume_tasks(self):
#         """
#         Start consuming messages from the 'gif_rpc_queue'.
#         """
#         self.channel.basic_consume(
#             queue=self.queue_name,
#             on_message_callback=lambda ch, method, props, body:
#             asyncio.run(self.on_request(ch, method, props, body))
#         )
#         print('[*] Waiting for messages. To exit press CTRL+C')
#         self.channel.start_consuming()
        
#     async def process_data(self, request_data):
#         """
#         Abstract method to be implemented by child classes to handle custom request processing.
#         """
#         raise NotImplementedError("Child classes must implement 'process_data' method.")
    