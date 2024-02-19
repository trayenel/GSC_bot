import configparser
import sys

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

config = configparser.ConfigParser()
file = None

if '-h' in opts:
    print(f"Usage:")
    raise SystemExit(f"Usage {sys.argv[0]} (-c | -h) <arguments>...")
elif "-c" in opts:
    for arg in args:
        file = open(arg, "r")
    config.read(file.name)
else:
    raise SystemExit(f"Usage {sys.argv[0]} (-c | -h) <arguments>...")

API_ID = config["TOKENS"]["api_id"]
API_HASH = config["TOKENS"]["api_hash"]
BOT_TOKEN = config["TOKENS"]["bot_token"]
