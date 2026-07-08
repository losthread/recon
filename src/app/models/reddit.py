from dataclasses import dataclass

@dataclass
class RedditProfile:
  username: str
  id: str
  karma: int
  comments: int
  posts: int

@dataclass
class RedditPost:
  id: int
  title: str
  body: str
  subreddit: str
  created_utc: int # unix time int