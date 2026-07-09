from argparse import ArgumentParser
from .fetchers.reddit import fetch_reddit_user_details, fetch_reddit_user_posts, fetch_reddit_user_comments
from .fetchers.github import fetch_github_user_details
from .fetchers.mastodon import fetch_mastodon_user_details, fetch_mastodon_user_statuses
from .fetchers.hackernews import fetch_hackernews_user, fetch_hackernews_user_posts

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
  reddit_user = fetch_reddit_user_details(username=args.username)
  reddit_user_posts = fetch_reddit_user_posts(username=args.username)
  reddit_user_comments = fetch_reddit_user_comments(username=args.username)

  # fetch github
  github_user = fetch_github_user_details(args.username)

  # fetch mastodon
  mastodon_user = fetch_mastodon_user_details(args.username)
  mastodon_user_posts = fetch_mastodon_user_statuses(args.username)

  # fetch hackernews
  hackernews_user = fetch_hackernews_user(args.username)
  hackernews_user_posts = fetch_hackernews_user_posts(args.username)

if __name__ == '__main__':
  main()