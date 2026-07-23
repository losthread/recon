from ..models.leetcode import LeetcodeProfile
from ..utils.common import assemble_profile, get_random_user_agent
from ..core.client import client
import asyncio
import httpx

# leetcode provides a free no auth graphql endpoint 
# to get the user's profile with their username

BASE_URL = 'https://leetcode.com/graphql'

# fetch the user's profile
async def fetch_leetcode_user_details(username: str) -> LeetcodeProfile | None:
  headers = {
    "User-Agent": get_random_user_agent(),
    "Accept": "application/json, text/plain, */*",
  }

  # post request
  payload = {
    "query": "query getUserProfile($username: String!) { matchedUser(username: $username) { username profile { realName userAvatar aboutMe countryName ranking reputation } } }",
    "variables": {
        "username": f"{username}"
    }
  }

  try:
    response = await client.post(
      BASE_URL,
      headers=headers,
      json=payload
    )
    response.raise_for_status()

  # catch http errors
  except httpx.HTTPError:
    return None

  # convert json to dict
  data = response.json().get("data", {})
  if not data:
    return None 

  matched_user = data.get("matchedUser")
  if not matched_user:
    return None

  profile = matched_user.get("profile") or {}

  return LeetcodeProfile(
    username=matched_user.get("username") or username,
    name=profile.get("realName") or "",
    avatar_url=profile.get("userAvatar") or "",
    bio=profile.get("aboutMe") or "",
    location=profile.get("countryName") or ""
  )

async def fetch_and_assemble_leetcode(username: str) -> dict | None:
  leetcode_user = await fetch_leetcode_user_details(username)

  if not leetcode_user:
    return None

  return assemble_profile(
    base={
      'platform': 'leetcode',
      'username': leetcode_user.username,
      'name': leetcode_user.name,
      'avatar_url': leetcode_user.avatar_url,
      'bio': leetcode_user.bio,
      'location': leetcode_user.location
    },
    items=[]
  )