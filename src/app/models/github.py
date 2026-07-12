from dataclasses import dataclass

@dataclass
class GithubProfile:
  username: str
  id: str
  name: str
  profile_url: str
  avatar_url: str
  bio: str
  followers: int
  folowing: int
  location: str
  company: str
  blog: str
  email: str
  twitter_username: str
  created_utc: int # convert iso to utc unix time