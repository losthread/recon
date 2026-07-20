from ..models.hackernews import HackernewsProfile, HackernewsPost
from ..utils.common import assemble_profile
from ..core.client import client
import asyncio
import httpx

# fetch user profile and karma
async def fetch_hackernews_user(username: str):
  url = f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
  
  try:
    # raise error if occured when fetching
    response = await client.get(url)
    response.raise_for_status()
  except httpx.HTTPError:
    return None
  
  # convert json to dict
  user = response.json()

  if user is None:
    return None
  
  return HackernewsProfile(
    username=user.get("id"),
    karma=user.get("karma"),
    created_utc=user.get("created"),
    bio=user.get("about"),
  )

# fetch user's posts (submissions)
async def fetch_hackernews_user_posts(username: str, limit: int = 10):
  url = f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
  
  try:
    # raise error if occured when fetching
    response = await client.get(url)
    response.raise_for_status()
  except httpx.HTTPError:
    return []
  
  # convert json to dict
  user = response.json()
  # get submission ids (limited to specified limit)
  submission_ids = user.get("submitted", [])[:limit]
  
  posts = []
  for post_id in submission_ids:
    post_url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json"
    try:
      # fetch individual post
      post_response = await client.get(post_url)
      post_response.raise_for_status()
      post = post_response.json()
      posts.append(HackernewsPost(
        id=post.get("id"),
        title=post.get("title"),
        url=post.get("url"),
        created_utc=post.get("time"),
      ))
    except Exception:
      continue
  
  return posts

async def fetch_and_assemble_hackernews(username: str):
  hackernews_user, hackernews_user_posts = await asyncio.gather(
    fetch_hackernews_user(username),
    fetch_hackernews_user_posts(username)
  )

  hackernews_user_posts = hackernews_user_posts or []

  if not hackernews_user:
    return None

  return assemble_profile(
    base={
      'platform': 'hackernews',
      'username': hackernews_user.username,
      'karma': hackernews_user.karma,
      'bio': hackernews_user.bio,
      'created_utc': hackernews_user.created_utc,
      'profile_url': f'https://news.ycombinator.com/user?id={hackernews_user.username}'
    },
    items=hackernews_user_posts
  )