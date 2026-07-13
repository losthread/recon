from ..fetchers.reddit import fetch_and_assemble_reddit
from ..fetchers.github import fetch_and_assemble_github
from ..fetchers.mastodon import fetch_and_assemble_mastodon
from ..fetchers.hackernews import fetch_and_assemble_hackernews
from .patterns import EMAIL_REGEX, SOCIAL_PATTERNS, extract_social_handles

# core heuristics engine, that finds links between profiles and 
def find_relations(username: str):
  reddit_profile = fetch_and_assemble_reddit(username)
  github_profile = fetch_and_assemble_github(username)
  mastodon_profile = fetch_and_assemble_mastodon(username)
  hackernews_profile = fetch_and_assemble_hackernews(username)

  