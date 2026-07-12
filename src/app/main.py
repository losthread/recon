from argparse import ArgumentParser
from .fetchers.reddit import fetch_and_assemble_reddit
from .fetchers.github import fetch_and_assemble_github
from .fetchers.mastodon import fetch_and_assemble_mastodon
from .fetchers.hackernews import fetch_and_assemble_hackernews

CYAN = "\033[36m"
RESET = "\033[0m"

banner = f"""{CYAN}
 _____  ______ _____ ____  _   _ 
|  __ \|  ____/ ____/ __ \| \ | |
| |__) | |__ | |   | |  | |  \| |
|  _  /|  __|| |   | |  | | . ` |
| | \ \| |___| |___| |__| | |\  |
|_|  \_\______\_____\____/|_| \_|
{RESET}"""

print(banner)

# instantiate argument parser
parser = ArgumentParser()

def main():
  parser.add_argument('-u', '--username', help='Username to search')
  parser.add_argument('-e', '--email', help='Email (optional)')
  parser.add_argument('-n', '--name', help='Name (optional)')

  args = parser.parse_args()

  # fetch reddit
  # reddit_profile = fetch_and_assemble_reddit(args.username)

  # fetch github
  # github_profile = fetch_and_assemble_github(args.username)

  # fetch mastodon
  # mastodon_profile = fetch_and_assemble_mastodon(args.username)

  # fetch hackernews
  hackernews_profile = fetch_and_assemble_hackernews(args.username)

  # print(reddit_profile)
  print()

  print(hackernews_profile)
  print()

if __name__ == '__main__':
  main()