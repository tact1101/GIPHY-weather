from pydantic import BaseModel
from typing import Optional

class GIFRequestModel(BaseModel):
    tag: Optional[str] = None
    rating: Optional[str] = "pg-13"

class GIFResponseModel(BaseModel):
    gif_url: str
    title: str