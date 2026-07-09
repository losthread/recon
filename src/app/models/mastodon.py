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
  created_at: str # iso format

@dataclass
class MastodonPost:
  id: str
  content: str
  created_at: str
  replies_count: int