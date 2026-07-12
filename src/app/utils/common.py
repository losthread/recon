from datetime import datetime

# user agent to clarify tool
USER_AGENT = "recon/1.0.0 (privacy)" 

# normalize iso to utc time
def iso_to_utc(iso_string: str) -> int:
  dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
  return int(dt.timestamp())

# return active time period and sorted posts, comments by latest first
def assemble_profile(base, items):
  sorted_items = sorted(items, key=lambda x: x.created_utc, reverse=True)

  return {
    **base, #unpack base
    "items": sorted_items,
    "first_utc": sorted_items[-1].created_utc if sorted_items else None,
    "last_utc": sorted_items[0].created_utc if sorted_items else None,
  }