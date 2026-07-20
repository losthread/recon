from argparse import ArgumentParser
from .core.linker import heuristics
from rich.console import Console
from colorama import Fore
import asyncio

CYAN = "\033[36m"
RESET = "\033[0m"

banner = f"""{Fore.CYAN}
 _____  ______ _____ ____  _   _ 
|  __ \|  ____/ ____/ __ \| \ | |
| |__) | |__ | |   | |  | |  \| |
|  _  /|  __|| |   | |  | | . ` |
| | \ \| |___| |___| |__| | |\  |
|_|  \_\______\_____\____/|_| \_|
{Fore.RESET}"""

print(banner)

# instantiate argument parser
parser = ArgumentParser()
parser.add_argument('-u', '--username', help='Username to search')
parser.add_argument('-e', '--email', help='Email (optional)')

# instantiate console (for loading screen)
console = Console()

async def main():
  args = parser.parse_args()

  with console.status("[violet]Fetching profiles..."):
    prof = await heuristics(args.username)

  console.print(f"[bold violet]Disclaimer: Recon correlates public profiles using heuristics. Users on different platforms may share the same username, and some users intentionally use different usernames. Verify matches before drawing conclusions.")
  console.print(f"[bold cyan]Username:[/bold cyan] {prof['username']}")
  console.print(f"[bold cyan]Found On:[/bold cyan] {', '.join(prof['usernames_matched_on'])}")
  console.print(f"[bold cyan]Name:[/bold cyan] {prof['name'] or '-'}")

  if prof["emails"]:
    console.print("[bold cyan]Emails:[/bold cyan]")
    for email in prof["emails"]:
      console.print(f"  • {email}")

  if prof["locations"]:
    console.print("[bold cyan]Locations:[/bold cyan]")
    for location in prof["locations"]:
      console.print(f"  • {location}")

  if prof["socials"]:
    console.print("[bold cyan]Connected Profiles:[/bold cyan]")
    for social in prof["socials"]:
      console.print(f"  • {social.platform:<10} {social.url}")

def cli():
  asyncio.run(main())