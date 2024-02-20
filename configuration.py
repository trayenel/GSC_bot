import configparser
import sys
import validators

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

def validateUrl(url):
    if validators.domain(url) or validators.url(url):
        return True
    return False

config = configparser.ConfigParser()
file = None

if '-h' in opts:
    print(f"Usage:")
    raise SystemExit(f"Usage {sys.argv[0]} (-c | -h) <arguments>...")
elif "-c" in opts:
    file = open(args[-1], "r")
    config.read(file.name)
else:
    raise SystemExit(f"Usage {sys.argv[0]} (-c | -h) <arguments>...")

API_ID = config["TOKENS"]["api_id"]
API_HASH = config["TOKENS"]["api_hash"]
BOT_TOKEN = config["TOKENS"]["bot_token"]
