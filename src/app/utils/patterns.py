import re
from ..models.handle import SocialHandle

# Email regex
EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

# username regex patterns
USERNAME_PATTERNS = [
  r"^{username}$",       # Exact match
  r".*{username}.*",     # Substring
  r"^{username}[_-].*",  # prefix_something
  r".*[_-]{username}$",  # something_suffix
  r"^{username}\d+$",    # username123
]

# links regex patterns
SOCIAL_PATTERNS = [
  {
    "platform": "linkedin",
    "pattern": r"https?:\/\/(?:[\w-]+\.)?linkedin\.com\/in\/([A-Za-z0-9_-]+)",
  },
  {
    "platform": "x",
    "pattern": r"https?:\/\/(?:www\.|mobile\.)?(?:twitter\.com|x\.com)\/([A-Za-z0-9_]+)(?=\b|\/|$)",
    "reject": r"^(home|search|explore|intent|share|hashtag|notifications|messages|settings|i|compose|login|signup|tos|privacy|about)$",
  },
  {
    "platform": "github",
    "pattern": r"https?:\/\/(?:www\.)?github\.com\/([A-Za-z0-9][A-Za-z0-9-]{0,38})(?=\b|\/|$)",
    "reject": r"^(issues|pull|search|trending|marketplace|orgs|topics|collections|notifications|settings|new|features|pricing|enterprise|sponsors|readme|about|contact|login|join|signup|security|nonprofit|customer-stories|events|codespaces|copilot)$",
  },
  {
    "platform": "youtube",
    "pattern": r"https?:\/\/(?:www\.)?youtube\.com\/(?:@|channel\/|user\/|c\/)([A-Za-z0-9_-]+)",
  },
  {
    "platform": "instagram",
    "pattern": r"https?:\/\/(?:www\.)?instagram\.com\/([A-Za-z0-9_.]+)(?=\b|\/|$)",
    "reject": r"^(p|reel|tv|accounts|explore|stories|about|developer)$",
  },
  {
    "platform": "bluesky",
    "pattern": r"https?:\/\/(?:www\.)?bsky\.app\/profile\/([A-Za-z0-9_.:-]+)",
  },
  {
    "platform": "reddit",
    "pattern": r"https?:\/\/(?:www\.|old\.)?reddit\.com\/(?:u|user)\/([A-Za-z0-9_-]+)",
  },
  {
    "platform": "hackernews",
    "pattern": r"https?:\/\/news\.ycombinator\.com\/user\?id=([A-Za-z0-9_-]+)",
  },
  {
    "platform": "telegram",
    "pattern": r"https?:\/\/(?:www\.)?t\.me\/([A-Za-z0-9_]+)",
    "reject": r"^(joinchat|s)$",
  },
  {
    "platform": "gitlab",
    "pattern": r"https?:\/\/(?:www\.)?gitlab\.com\/([A-Za-z0-9][A-Za-z0-9_-]+)(?=\b|\/|$)",
    "reject": r"^(explore|help|users|projects|search|public|dashboard|admin)$",
  },
  {
    "platform": "stackoverflow",
    "pattern": r"https?:\/\/stackoverflow\.com\/users\/(\d+)",
  },
  {
    "platform": "mastodon",
    "pattern": r"https?:\/\/(mastodon\.[a-z.]+|mstdn\.[a-z.]+|fosstodon\.org|hachyderm\.io|infosec\.exchange)\/@([A-Za-z0-9_]+)",
  },
  {
    "platform": "facebook",
    "pattern": r"https?:\/\/(?:www\.|m\.|touch\.)?facebook\.com\/(?:profile\.php\?id=\d+|pages\/[^\/]+\/\d+|groups\/[^\/]+|([A-Za-z0-9.]+))(?=\b|\/|$)",
    "reject": r"^(home|login|signup|recover|help|policies|privacy|pages|groups|marketplace|watch|gaming|events|ads|creators)$",
  },
  {
    "platform": "discord",
    "pattern": r"https?:\/\/(?:www\.)?(?:discord\.com|discordapp\.com)\/(?:users|channels)\/(\d{17,20})",
  },
  {
    "platform": "tiktok",
    "pattern": r"https?:\/\/(?:www\.)?tiktok\.com\/@([A-Za-z0-9_.-]+)",
  },
  {
    "platform": "email",
    "pattern": r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
  },
  {
    "platform": "twitch",
    "pattern": r"https?:\/\/(?:www\.)?twitch\.tv\/([A-Za-z0-9_]{4,25})(?=\b|\/|$)",
    "reject": r"^(directory|videos|clips|moderator|popout|p|videos|jobs|press|store|legal|turbo)$",
  },
  {
    "platform": "medium",
    "pattern": r"https?:\/\/(?:www\.)?medium\.com\/@([A-Za-z0-9_.-]+)",
  },
  {
    "platform": "patreon",
    "pattern": r"https?:\/\/(?:www\.)?patreon\.com\/([A-Za-z0-9_-]+)(?=\b|\/|$)",
    "reject": r"^(home|login|signup|explore|create|pricing|about|legal|privacy)$",
  }
]

# extract social media links from given string 
def extract_social_handles(text: str) -> list[SocialHandle]:
  if not text:
    return []
  
  handles = list()
  # dont add duplicates
  seen = set()

  # match text against every regex
  for pattern_info in SOCIAL_PATTERNS:
    platform = pattern_info.get('platform')
    pattern = pattern_info.get('pattern')
    reject = pattern_info.get('reject')

    for match in re.finditer(pattern, text, re.IGNORECASE):
      # mastodon handle = m[2]@m[1], for others: handle = m[1]
      if platform == 'mastodon':
        handle = match.group(2) + '@' + match.group(1)
      else:
        handle = match.group(1)

      # reject useless links like login etc
      if reject and re.match(reject, handle, re.IGNORECASE):
        continue

      # if duplicate link found
      key = f'{platform}:{handle.lower()}'
      if key in seen:
        continue

      # else add key to set 
      seen.add(key)

      # append external handle to list if not rejected
      handles.append(SocialHandle(
        platform=platform,
        username=handle,
        url=match.group(0)
      ))

  return handles