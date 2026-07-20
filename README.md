# Recon
A Deterministic CLI OSINT tool to identify someone based on their public social profiles and history given their username/email.

## Features
- Search usernames across multiple platforms
- Fetch public profile metadata
- Aggregate posts and comments (where available)
- Extract emails and connected social profiles
- Correlate identities using heuristic matching

## Supported Platforms
- Reddit
- GitHub
- Mastodon
- Hacker News

## Tech Stack

- Python
- httpx
- asyncio
- dataclasses
- Rich
- BeautifulSoup *(planned)*
- LLM-based identity correlation *(planned)*

## Installation

### Clone the repository

```bash
git clone https://github.com/losthread/recon.git
cd recon
```

### Create a virtual environment
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Install dependencies
```bash
pip install -e .
```

## Usage
Search by username:

```bash
recon -u <username>
```

## Note
Search by email support will be added in future

## How It Works
1. Fetch profiles from supported platforms concurrently.
2. Normalize profile data into a common format.
3. Extract emails and connected social accounts.
4. Deduplicate discovered identities.
5. Correlate usernames, names, emails, locations, and linked accounts.
6. Return aggregated evidence for further analysis.

## Disclaimer
Recon uses publicly available information and heuristic-based correlation to identify potentially related profiles. Results are not guaranteed to be accurate and may contain false positives or false negatives. Always verify findings independently before drawing conclusions or taking action.

This tool is intended for legitimate security research, OSINT, educational, and investigative purposes only. Users are solely responsible for ensuring their use complies with applicable laws, regulations, and the terms of service of the platforms being queried.

The author assumes no responsibility or liability for any misuse of this software or for any damages resulting from its use.

## License
MIT