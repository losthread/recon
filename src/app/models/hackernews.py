from dataclasses import dataclass

@dataclass
class HackernewsProfile:
  username: str
  karma: int
  created_utc: int # convert iso to utc unix time
  bio: str

@dataclass
class HackernewsPost:
  id: int
  title: str
  url: str
  created_utc: int # convert iso to utc unix time