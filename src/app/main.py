from argparse import ArgumentParser
from .core.linker import find_relations

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

  find_relations(args.username)

if __name__ == '__main__':
  main()