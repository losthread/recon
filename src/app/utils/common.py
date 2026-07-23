from datetime import datetime
import random

# user agent to clarify tool
USER_AGENT = "recon/1.0.0 (privacy)" 

# normalize iso to utc time
def iso_to_utc(iso_string: str) -> int:
  dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
  return int(dt.timestamp())

# get a random user agent
def get_random_user_agent():
  agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/19.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 19_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/19.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36",
  ]
  random_agent = random.choice(agents)
  return random_agent

# return active time period and sorted posts, comments by latest first
def assemble_profile(base, items):
  sorted_items = sorted(items, key=lambda x: x.created_utc, reverse=True)

  return {
    **base, #unpack base
    "items": sorted_items,
    "first_utc": sorted_items[-1].created_utc if sorted_items else None,
    "last_utc": sorted_items[0].created_utc if sorted_items else None,
  }