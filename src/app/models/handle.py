from dataclasses import dataclass

@dataclass
class SocialHandle:
  platform: str
  username: str
  url: str