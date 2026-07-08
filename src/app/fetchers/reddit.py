import requests
# using arctic shift to fetch reddit data
# it is a community archive and doesnt need auth

BASE_URL = 'https://arctic-shift.photon-reddit.com/api'

# fetch user metadata (bio, username)
def fetch_reddit_user_details(username: str):
  URL = f'{BASE_URL}/users/search'
  # querystring params
  params = {'author': username}
  
  # raise error if occured when fetching
  response = requests.get(URL, params=params)
  response.raise_for_status()
  
  # convert json to dict
  data = response.json()["data"]
  if not data:
    return None
  
  # returns a list of dicts
  user = data[0]

  return {
    "username": user["author"],
    "id": user["id"],
    "karma": user["_meta"]["total_karma"],
    "comments": user["_meta"]["num_comments"],
    "posts": user["_meta"]["num_posts"],
  }