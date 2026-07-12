import requests
from ..models.mastodon import MastodonProfile, MastodonPost
from ..utils.common import iso_to_utc, USER_AGENT, assemble_profile

BASE_URL = "https://mastodon.social/api/v1"

# fetch user profile
def fetch_mastodon_user_details(username: str) -> MastodonProfile:
  # querystring params
  params = {
    'acct': username
  }

  try:
    # raise error if occured when fetching
    response = requests.get(f'{BASE_URL}/accounts/lookup', params=params, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
  except requests.exceptions.HTTPError:
    return None
  
  # convert json to dict
  user = response.json()

  return MastodonProfile(
    id=user.get('id'),
    username=user.get('username'),
    name=user.get('display_name'),
    bio=user.get('note'),
    url=user.get('url'),
    avatar_url=user.get('avatar'),
    followers=user.get('followers_count', 0),
    following=user.get('following_count', 0),
    posts=user.get('statuses_count', 0),
    created_utc=iso_to_utc(user.get('created_at')),
  )

# posts on mastodon are called statuses and comments are nested NOT SEPARATE
# fetch statuses
def fetch_mastodon_user_statuses(username: str, limit: int = 40) -> list[MastodonPost]:
  try:
    # get user id (required for status searching endpoint)
    user_lookup = requests.get(f'{BASE_URL}/accounts/lookup', params={'acct': username}, headers={"User-Agent": USER_AGENT})
    user_lookup.raise_for_status()
    user_id = user_lookup.json()['id']

    # get their statuses(posts)
    response = requests.get(f'{BASE_URL}/accounts/{user_id}/statuses', params={'limit': limit}, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()

  except requests.exceptions.HTTPError:
    return []
  
  posts = list()
  for status in response.json():
    posts.append(MastodonPost(
      id=status.get('id'),
      content=status.get('content'),
      created_utc=iso_to_utc(status.get('created_at')),
      replies_count=status.get('replies_count', 0),
    ))

  return posts

def fetch_and_assemble_mastodon(username: str):
  mastodon_user = fetch_mastodon_user_details(username)
  if not mastodon_user:
    return None

  mastodon_user_posts = fetch_mastodon_user_statuses(username) or []

  return assemble_profile(
    base={
      'platform': 'mastodon',
      'username': mastodon_user.username,
      'profile_url': mastodon_user.url,
    },
    items=mastodon_user_posts
  )