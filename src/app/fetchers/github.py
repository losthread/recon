import requests
from ..models.github import GithubProfile
from ..utils.common import iso_to_utc, USER_AGENT, assemble_profile

BASE_URL = "https://api.github.com"

# fetch user profile
def fetch_github_user_details(username: str) -> GithubProfile:
  try:
    # raise error if occured when fetching
    response = requests.get(f'{BASE_URL}/users/{username}', headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
  except requests.exceptions.HTTPError:
    return None

  # convert json to dict
  user = response.json()

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
    twitter_username=user.get("twitter_username"),
    created_utc=iso_to_utc(user.get("created_at")),
  )

def fetch_and_assemble_github(username: str):
  github_user = fetch_github_user_details(username)
  if not github_user:
    return None

  return assemble_profile(
    base={
      'platform': 'github',
      'username': github_user.username,
      'profile_url': github_user.profile_url,
    },
    items=[]
  )