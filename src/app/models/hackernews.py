from dataclasses import dataclass

@dataclass
class HackernewsProfile:
  username: str
  karma: int
  created_at: int
  bio: str

@dataclass
class HackernewsPost:
  id: int
  title: str
  url: str
  created_at: int