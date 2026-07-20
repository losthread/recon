from ..models.mastodon import MastodonProfile, MastodonPost
from ..utils.common import iso_to_utc, assemble_profile
from ..core.client import client
import asyncio
import httpx

BASE_URL = "https://mastodon.social/api/v1"

# fetch user profile
async def fetch_mastodon_user_details(username: str) -> MastodonProfile | None:
  # querystring params
  params = {
    'acct': f'{username}@mastodon.social'
  }

  try:
    # raise error if occured when fetching
    response = await client.get(f'{BASE_URL}/accounts/lookup', params=params)
    response.raise_for_status()
  except httpx.HTTPError:
    return None
  
  # convert json to dict
  user = response.json()

  fields = user.get('fields', [])
  fields_text = ' '.join([f.get('value', '') for f in fields])

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
    fields=fields_text,
    created_utc=iso_to_utc(user.get('created_at')),
  )

# posts on mastodon are called statuses and comments are nested NOT SEPARATE
# fetch statuses
async def fetch_mastodon_user_statuses(username: str, limit: int = 40) -> list[MastodonPost]:
  try:
    # get user id (required for status searching endpoint)
    user_lookup = await client.get(f'{BASE_URL}/accounts/lookup', params={'acct': username})
    user_lookup.raise_for_status()
    user_id = user_lookup.json()['id']

    # get their statuses(posts)
    response = await client.get(f'{BASE_URL}/accounts/{user_id}/statuses', params={'limit': limit})
    response.raise_for_status()

  except httpx.HTTPError:
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

async def fetch_and_assemble_mastodon(username: str):
  mastodon_user, mastodon_user_posts = await asyncio.gather(
    fetch_mastodon_user_details(username),
    fetch_mastodon_user_statuses(username)
  )

  if not mastodon_user:
    return None
  
  mastodon_user_posts = mastodon_user_posts or []

  return assemble_profile(
    base={
      'platform': 'mastodon',
      'username': mastodon_user.username,
      'profile_url': mastodon_user.url,
      'id': mastodon_user.id,
      'name': mastodon_user.name,
      'bio': mastodon_user.bio,
      'avatar_url': mastodon_user.avatar_url,
      'followers': mastodon_user.followers,
      'following': mastodon_user.following,
      'posts': mastodon_user.posts,
      'fields': mastodon_user.fields,
      'created_utc': mastodon_user.created_utc,
    },
    items=mastodon_user_posts
  )