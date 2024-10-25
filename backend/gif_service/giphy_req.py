from urllib import parse
from fastapi import HTTPException
from pydantic import BaseModel
import aiohttp
from common.api_key import KEY
import logging

class GIF_request(BaseModel):
    tag: str = None
    rating: str = "pg-13"
    

async def fetch_random_gif(tag: str = ModuleNotFoundError) -> dict:
    """
    Fetch random GIF based on a search tag .
    
    Args:
        query (str): The search term for the GIF.

    Returns:
        dict: The JSON response from the Giphy API.
        
        Example: {"gif_url": gif_url, "title": title}
    """
    
    url = "http://api.giphy.com/v1/gifs/random"
    params = parse.urlencode({
        "api_key": KEY,
        "tag": tag,
        "rating": "pg-13",
    })
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{url}?{params}") as resp:
                if resp.status != 200:
                    raise HTTPException(status=resp.status, detail="Error fetching a GIF.")
                data = await resp.json()
            if data['data']:
                gif_url = data['data']['images']['original']['url']
                title = data['data']['title']
                logging.info(f"gif_url: {gif_url}, title: {title}")
                return {"gif_url": gif_url, "title": title}
            else:
                print("No GIFs found for this query.")
                logging.info("No GIFs found for this query.")
                raise HTTPException(status_code=504, detail="Error fetching a gif.")
        except aiohttp.ClientError as e:
            logging.error(f"Error fetching a GIF {str(e)}")
            raise HTTPException(status_code=504, detail="Error fetching a GIF.") from e

# import asyncio
# import json

# async def main():
#     try:
#         result = await fetch_gif("goodbye")
#         print(result)
#     except HTTPException as e:
#         print(f"Error: {e.detail}")

# # Run the async main function
# asyncio.run(main())
