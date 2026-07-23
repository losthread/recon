from ..models.github import GithubProfile
from ..utils.common import iso_to_utc, assemble_profile, get_random_user_agent
from ..core.client import client
import httpx
import asyncio

BASE_URL = "https://api.github.com"

# fetch user profile
async def fetch_github_user(username: str) -> dict | None:
  try:
    response = await client.get(
      f"{BASE_URL}/users/{username}",
      headers={"User-Agent": get_random_user_agent()},
    )
    response.raise_for_status()
    return response.json()
  except httpx.HTTPError:
    return None


async def fetch_github_socials(username: str) -> list:
  try:
    response = await client.get(
      f"{BASE_URL}/users/{username}/social_accounts",
      headers={"User-Agent": get_random_user_agent()},
    )
    response.raise_for_status()
    return response.json()
  except httpx.HTTPError:
    return []


async def fetch_github_readme(username: str) -> str:
  try:
    response = await client.get(
        f"{BASE_URL}/repos/{username}/{username}/readme",
        headers={
          "User-Agent": get_random_user_agent(),
          "Accept": "application/vnd.github.raw+json",
        },
    )
    response.raise_for_status()
    return response.text
  except httpx.HTTPError:
    return ""
    
async def fetch_github_user_details(username: str) -> GithubProfile | None:
  user, socials_data, readme_text = await asyncio.gather(
    fetch_github_user(username),
    fetch_github_socials(username),
    fetch_github_readme(username),
  )

  if not user:
    return None

  return GithubProfile(
    username=user.get("login"),
    id=user.get("id"),
    name=user.get("name"),
    avatar_url=user.get("avatar_url"),
    profile_url=f"https://github.com/{user.get('login')}",
    bio=user.get("bio"),
    followers=user.get("followers", 0),
    folowing=user.get("following", 0),
    location=user.get("location"),
    company=user.get("company"),
    blog=user.get("blog"),
    email=user.get("email"),
    social_accounts=socials_data,
    readme=readme_text,
    created_utc=iso_to_utc(user.get("created_at")),
  )

async def fetch_and_assemble_github(username: str) -> dict | None:
  github_user = await fetch_github_user_details(username)
  if not github_user:
    return None

  return assemble_profile(
    base={
      'platform': 'github',
      'username': github_user.username,
      'id': github_user.id,
      'name': github_user.name,
      'avatar_url': github_user.avatar_url,
      'profile_url': github_user.profile_url,
      'bio': github_user.bio,
      'followers': github_user.followers,
      'following': github_user.folowing,
      'location': github_user.location,
      'company': github_user.company,
      'blog': github_user.blog,
      'email': github_user.email,
      'socials': github_user.social_accounts,
      'readme': github_user.readme,
      'created_utc': github_user.created_utc,
    },
    items=[]
  )