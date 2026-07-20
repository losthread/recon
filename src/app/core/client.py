from ..utils.common import USER_AGENT
import httpx

client = httpx.AsyncClient(
  headers={
    'User-Agent': USER_AGENT
  },
  timeout=10.0,
  follow_redirects=True
)