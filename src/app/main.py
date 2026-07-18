from argparse import ArgumentParser
from .core.linker import heuristics
from colorama import Fore

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

def main():
  parser.add_argument('-u', '--username', help='Username to search')
  parser.add_argument('-e', '--email', help='Email (optional)')

  args = parser.parse_args()

  prof = heuristics(args.username)
  print(prof)

if __name__ == '__main__':
  main()