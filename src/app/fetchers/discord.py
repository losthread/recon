from ..core.client import client
from ..utils.common import get_random_user_agent
import httpx
### discord does not allow fetching a profile 
# so we can only check if a user exists or not
# by checking if the provided username is taken or not

URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

async def fetch_discord_username(username: str):
  headers = {
    "User-Agent": get_random_user_agent(),
    "authority": "discord.com",
    "accept": "/",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "origin": "https://discord.com",
    "referer": "https://discord.com/register",
  }

  # accepts a post request
  payload = {
    "username": username
  }

  try:
    response = await client.post(URL, json=payload, headers=headers)

    # username taken means target found
    if response.status_code == 200:
      return {
        "platform": 'discord',
        "username": username,
        "profile_url": 'https://discord.com/',
        "found": True,
      }
    
    # username not taken means target not found
    return {
      "found": False
    }
  
  except httpx.HTTPError: 
    return None