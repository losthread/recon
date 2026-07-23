from ..core.client import client
from ..utils.common import get_random_user_agent
import httpx

# Proton exposes an availability API used by their web account app.
# IT DOES NOT give any user details, just checks existence
# - Code 12106: username exists (taken)
# - Code 1000: username does not exist (available)

async def check_protonmail_username(username: str) -> dict:
  url = (
    "https://account.proton.me/api/core/v4/users/available"
    f"?Name={username}%40proton.me&ParseDomain=1"
  )
  headers = {
    "User-Agent": get_random_user_agent(),
    "x-pm-appversion": "web-mail@6.0.1.3",
    "Accept": "application/json",
  }
  
  try:
    response = await client.get(
    url,
    headers={
      **client.headers,
      "User-Agent": headers["User-Agent"],
      "x-pm-appversion": "web-mail@6.0.1.3",
      "Accept": "application/json",
    }
  )
    data = response.json()
    code = data.get("Code")
    
    if code == 12106:
      return {
        "platform": 'protonmail',
        "username": username,
        "found": True,
      }
    if code == 1000:
    # Username available
      return {
        "found": False
      }   
    
    return None     # Unknown
  
  except httpx.HTTPError:
    return None