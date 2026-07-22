from ..fetchers.reddit import fetch_and_assemble_reddit
from ..fetchers.github import fetch_and_assemble_github
from ..fetchers.mastodon import fetch_and_assemble_mastodon
from ..fetchers.hackernews import fetch_and_assemble_hackernews
from ..fetchers.discord import fetch_discord_username
from ..utils.patterns import USERNAME_PATTERNS, extract_social_handles
from ..models.handle import SocialHandle
from collections import Counter
import asyncio
import re

async def fetch_profiles(username: str):
  return await asyncio.gather(
    fetch_and_assemble_reddit(username),
    fetch_and_assemble_github(username),
    fetch_and_assemble_mastodon(username),
    fetch_and_assemble_hackernews(username),
    fetch_discord_username(username),
  )

async def find_links(username: str):
  profiles = await fetch_profiles(username)

  # social links connected or mentioned on profiles
  social_links: list[SocialHandle] = []

  for profile in profiles:
    if not profile:
      continue

    # extract links from github
    if profile.get('platform') == 'github':
      # find explicit social links to profiles
      if 'socials' in profile:
        for account in profile['socials']:
          url = account.get('url')
          # get a standardized model (returns a list)
          extracted = extract_social_handles(url)
          social_links.extend(extracted)

      # extract any links from the bio
      if 'bio' in profile:
        social_links.extend(extract_social_handles(profile.get('bio')))

      # extract any links from the user's readme.md
      if 'readme' in profile:
        social_links.extend(extract_social_handles(profile.get('readme')))

    # extract links from mastodon
    if profile.get('platform') == 'mastodon':
      # extract from bio
      if 'bio' in profile:
        social_links.extend(extract_social_handles(profile.get('bio')))

      # extract from dedicated links section
      if 'fields' in profile:
        social_links.extend(extract_social_handles(profile.get('fields')))

    # extract links from hackernews 
    if profile.get('platform') == 'hackernews' and 'bio' in profile:
      social_links.extend(extract_social_handles(profile.get('bio')))

  # arctic shift does not provide social links connected to reddit
  # need to scrape the page manually (inside scrapers/)

  # remove duplicate links
  seen = set()
  unique_links = []

  for link in social_links:
    key = (link.platform, link.username)

    if key in seen:
      continue
      
    seen.add(key)
    unique_links.append(link)

  return profiles, unique_links

### common fields to match
# username
# name
# email
# bio
# location
# email
# links

# match usernames
def username_match(original: str, candidate: str) -> bool:
  if not candidate:
    return False

  for pattern in USERNAME_PATTERNS:
    regex = pattern.format(username=re.escape(original))
    if re.match(regex, candidate, re.IGNORECASE):
      return True
  return False

# heuristics engine to find similarities between profiles
async def heuristics(username):
  profiles, links = await find_links(username)

  # matched username platforms
  matched_platforms = list()
  total_platforms = 0

  # all names
  names = list()
  # all emails
  emails = set()
  # locations
  locations = set()

  # find similarities in common fields across fetched platforms
  for profile in profiles:
    if not profile:
      continue

    total_platforms += 1

    # matched usernames
    if profile.get('username') and username_match(username, profile.get('username')):
      matched_platforms.append(profile['platform'])

    # extracted names
    if profile.get('name'):
      names.append(profile.get('name').lower().strip())

    # fetched emails
    if profile.get('email'):
      emails.add(profile.get('email').lower())

    # given locations
    if profile.get('location'):
      locations.add(profile.get('location').lower().strip())

  # pick the most common name across platforms (in case diff names are entered)
  most_common_name = Counter(names).most_common(1)[0][0] if names else None

  # add linked emails
  for link in links:
    if link.platform == 'email':
      emails.add(link.url.lower())

  return {
    'username': username,
    'usernames_matched_on': matched_platforms,
    'name': most_common_name,
    'emails': list(emails) if emails else None,
    'locations': list(locations) if locations else None,
    'socials': links if links else None
  }