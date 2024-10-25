from gif_service import gif_rpc_client 
from common.rabbitmq_connection import RabbitMQConnection
from fastapi import HTTPException, APIRouter
from gif_service.models import GIFRequestModel
import logging

router = APIRouter()

@router.post("/gif/get_gif")
async def send_gif_request(gif_request: GIFRequestModel) -> dict:
    """
    Receives a GIF request, and sends it to the RabbitMQ queue.
    Args:
        GIF_request: 
            tag: str = None
            rating: str = "pg-13"
            
    Returns:
        dict:
            {"gif_url": gif_url, "title": title}
    """
    try:
        rpc_client = gif_rpc_client.GIFRPCClient(RabbitMQConnection())
        response = rpc_client.request_gif(gif_request.model_dump())
        return response
    except Exception as e:
        logging.error(f"Error {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error sending task to queue: {str(e)}.") 