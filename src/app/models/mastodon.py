from dataclasses import dataclass

@dataclass
class MastodonProfile:
  id: str
  username: str
  name: str
  bio: str
  url: str
  avatar_url: str
  followers: int
  following: int
  posts: int
  created_utc: int # convert iso to utc unix time

@dataclass
class MastodonPost:
  id: str
  content: str
  created_utc: int # convert iso to utc unix time
  replies_count: int