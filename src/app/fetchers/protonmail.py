import requests
  # Proton exposes an availability API used by their web account app.

  # - Code 12106: username exists (taken)
  # - Code 1000: username does not exist (available)
def check_protonmail_username(username: str) -> bool:
  url = (
    "https://account.proton.me/api/core/v4/users/available"
    f"?Name={username}%40proton.me&ParseDomain=1"
  )
  headers = {
    "x-pm-appversion": "web-mail@6.0.1.3",
    "Accept": "application/json",
  }
  
  try:
    response = requests.get(url, headers=headers)
    data = response.json()
    code = data.get("Code")
    
    if code == 12106:
      return False  # Username taken
    if code == 1000:
      return True   # Username available
    return None     # Unknown
  
  except:
    return None