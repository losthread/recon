import requests
from ..models.reddit import RedditProfile, RedditPost, RedditComment
# using arctic shift to fetch reddit data
# it is a community archive and doesnt need auth

BASE_URL = 'https://arctic-shift.photon-reddit.com/api'

# fetch user metadata (bio, username)
def fetch_reddit_user_details(username: str) -> RedditProfile:
  URL = f'{BASE_URL}/users/search'
  # querystring params
  params = {'author': username}
  
  try:
    # raise error if occured when fetching
    response = requests.get(URL, params=params)
    response.raise_for_status()
  # catch any http error  
  except requests.exceptions.HTTPError:
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

# fetch user's top 100 posts
def fetch_reddit_user_posts(username: str, limit: int = 100) -> list[RedditPost]:
  URL = f'{BASE_URL}/posts/search'
  # querystring params
  params = {
    'author': username,
    'limit': limit,
    'sort': 'desc'
  }
  
  try:
    # raise error if occured when fetching
    response = requests.get(URL, params=params)
    response.raise_for_status()
  except requests.exceptions.HTTPError:
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

# fetch user's top 100 comments 
def fetch_reddit_user_comments(username: str, limit: int = 100) -> list[RedditComment]:
  URL = f'{BASE_URL}/comments/search'
  # querystring params
  params = {
    'author': username,
    'limit': limit,
    'sort': 'desc',
  }

  try:
    # raise error if occrued
    response = requests.get(URL, params=params)
    response.raise_for_status()
  except requests.exceptions.HTTPError:
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