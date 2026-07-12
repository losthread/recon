import requests
from ..models.hackernews import HackernewsProfile, HackernewsPost
from ..utils.common import USER_AGENT, assemble_profile

# fetch user profile and karma
def fetch_hackernews_user(username: str):
  url = f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
  
  try:
    # raise error if occured when fetching
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
  except requests.exceptions.HTTPError:
    return None
  
  # convert json to dict
  user = response.json()
  
  return HackernewsProfile(
    username=user.get("id"),
    karma=user.get("karma"),
    created_utc=user.get("created"),
    bio=user.get("about"),
  )

# fetch user's posts (submissions)
def fetch_hackernews_user_posts(username: str, limit: int = 10):
  url = f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
  
  try:
    # raise error if occured when fetching
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
  except requests.exceptions.HTTPError:
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
      post_response = requests.get(post_url)
      post_response.raise_for_status()
      post = post_response.json()
      posts.append(HackernewsPost(
        id=post.get("id"),
        title=post.get("title"),
        url=post.get("url"),
        created_utc=post.get("time"),
      ))
    except:
      continue
  
  return posts

def fetch_and_assemble_hackernews(username: str):
  hackernews_user = fetch_hackernews_user(username)
  if not hackernews_user:
    return None

  hackernews_user_posts = fetch_hackernews_user_posts(username) or []

  return assemble_profile(
    base={
      'platform': 'hackernews',
      'username': hackernews_user.username,
      'profile_url': f'https://news.ycombinator.com/user?id={hackernews_user.username}'
    },
    items=hackernews_user_posts
  )