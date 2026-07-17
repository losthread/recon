import requests
from ..models.github import GithubProfile
from ..utils.common import iso_to_utc, USER_AGENT, assemble_profile

BASE_URL = "https://api.github.com"

# fetch user profile
def fetch_github_user_details(username: str) -> GithubProfile:
  # fetch profile
  try:
    response = requests.get(f'{BASE_URL}/users/{username}', headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
  except requests.exceptions.HTTPError:
    return None

  # fetch social links conected explicitly
  socials_data = []
  try:
    socials = requests.get(f'{BASE_URL}/users/{username}/social_accounts', headers={"User-Agent": USER_AGENT})
    socials.raise_for_status()
    socials_data = socials.json()
  except requests.exceptions.HTTPError:
    pass  # Optional

  # fetch social links from readme
  readme_text = ""
  try:
    readme_response = requests.get(
      f'{BASE_URL}/repos/{username}/{username}/readme',
      headers={'User-Agent': USER_AGENT, 'Accept': 'application/vnd.github.raw+json'}
    )
    readme_response.raise_for_status()
    readme_text = readme_response.text
  except requests.exceptions.HTTPError:
    pass # optional

  # convert json to dict
  user = response.json()
  socials_data = socials.json()

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

def fetch_and_assemble_github(username: str):
  github_user = fetch_github_user_details(username)
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