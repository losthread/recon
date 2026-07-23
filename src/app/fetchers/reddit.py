from ..models.reddit import RedditProfile, RedditPost, RedditComment
from ..utils.common import assemble_profile, get_random_user_agent
from ..core.client import client
import asyncio
import httpx

# using arctic shift to fetch reddit data
# it is a community archive and doesnt need auth

BASE_URL = 'https://arctic-shift.photon-reddit.com/api'

# fetch user metadata (bio, username)
async def fetch_reddit_user_details(username: str) -> RedditProfile | None:
  URL = f'{BASE_URL}/users/search'
  # querystring params
  params = {'author': username}
  
  try:
    # raise error if occured when fetching
    response = await client.get(
      URL,
      params=params,
      headers={'User-Agent': get_random_user_agent()},
    )
    response.raise_for_status()
  # catch any http error  
  except httpx.HTTPError:
    return None
  
  # convert json to dict
  data = response.json().get("data", [])
  if not data:
    return None
  
  # returns a list of dicts
  user = data[0]
  meta = user.get("_meta", {})

  return RedditProfile(
    username=user.get("author"),
    id=user.get("id"),
    karma=meta.get("total_karma", 0),
    comments=meta.get("num_comments", 0),
    posts=meta.get("num_posts", 0),
  )

# fetch user's recent 100 posts
async def fetch_reddit_user_posts(username: str, limit: int = 100) -> list[RedditPost] | None:
  URL = f'{BASE_URL}/posts/search'
  # querystring params
  params = {
    'author': username,
    'limit': limit,
    'sort': 'desc'
  }

  try:
    # raise error if occured when fetching
    response = await client.get(
      URL,
      params=params,
      headers={'User-Agent': get_random_user_agent()},
    )
    response.raise_for_status()

  except httpx.HTTPError:
    return None
  
  # convert json to dict
  data = response.json().get("data", [])

  if not data:
    return None

  posts = list()
  for post in data:
    posts.append(RedditPost(
      id=post.get("id"),
      title=post.get("title"),
      body=post.get("selftext"),
      subreddit=post.get("subreddit"),
      created_utc=post.get("created_utc"),
    ))
  
  return posts

# fetch user's recent 100 comments 
async def fetch_reddit_user_comments(username: str, limit: int = 100) -> list[RedditComment] | None:
  URL = f'{BASE_URL}/comments/search'
  # querystring params
  params = {
    'author': username,
    'limit': limit,
    'sort': 'desc',
  }

  try:
    # raise error if occrued
    response = await client.get(
      URL,
      params=params,
      headers={'User-Agent': get_random_user_agent()},
    )
    response.raise_for_status()
  except httpx.HTTPError:
    return None

  # convert json to dict
  data = response.json().get("data", [])

  if not data:
    return None

  comments = list()
  for comment in data:
    comments.append(RedditComment(
      id=comment.get('id'),
      body=comment.get('body'),
      subreddit=comment.get('subreddit'),
      created_utc=comment.get('created_utc'),
    ))

  return comments

# fetch profile, posts, comments and assemble it
async def fetch_and_assemble_reddit(username: str) -> dict | None:
  reddit_user, reddit_user_posts, reddit_user_comments = await asyncio.gather(
    fetch_reddit_user_details(username),
    fetch_reddit_user_posts(username),
    fetch_reddit_user_comments(username)
  )

  if not reddit_user:
    return None
  
  reddit_user_posts = reddit_user_posts or []
  reddit_user_comments = reddit_user_comments or []

  all_items = reddit_user_posts + reddit_user_comments
  
  return assemble_profile(
    base={
      'platform': 'reddit',
      'username': reddit_user.username,
      'id': reddit_user.id,
      'karma': reddit_user.karma,
      'comments': reddit_user.comments,
      'posts': reddit_user.posts,
      'profile_url': f'https://reddit.com/user/{reddit_user.username}',
    },
    items=all_items
  )