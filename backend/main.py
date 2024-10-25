from gif_service.gif_rpc_server import GIFRPCServer
from weather_service import weather_rpc_server
from common import rabbitmq_connection 
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from weather_service.weather_routes import router as weather_router
from gif_service.gif_routes import router as gif_router
    

import asyncio

# @asynccontextmanager
# async def start_rpc_servers(app: FastAPI):
#     logging.info("Starting RPC servers...")
#     connection = rabbitmq_connection.RabbitMQConnection()
    
#     if connection:
#         logging.info("RabbitMQ connection established.")
#     else:
#         logging.error("RabbitMQ connection failed.")
        
#     gif_rpc_server = GIFRPCServer(connection)
#     weather_local_rpc_server = weather_rpc_server.WeatherServer(connection)
    
#     await weather_local_rpc_server.consume_tasks()
#     await gif_rpc_server.consume_tasks()
#     yield


# app = FastAPI(lifespan=start_rpc_servers)
app = FastAPI()
    
# Include weather router
app.include_router(weather_router)
app.include_router(gif_router)



