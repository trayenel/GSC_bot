import pyrogram.errors
import argparse
import sys
import logging
import configparser
from bot import login


opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

logger = logging.getLogger("SR2_bot")

if "-h" in opts:
    print(f"Usage: {sys.argv[0]} [OPTIONS]")
    print(f"-c, --config FILE".ljust(20, " "), f"Specify a configuration file.")
    print(f"-h, --help".ljust(20, " "), f"Show this help message and exit.")

    raise SystemExit
elif "-c" in opts:
    try:
        config = configparser.ConfigParser()
        file = open(args[-1], "r")
        config.read(file.name)
    except (FileNotFoundError, IndexError):
        logging.error("Config file not found.")
        raise SystemExit
    except (configparser.MissingSectionHeaderError, configparser.NoOptionError):
        logging.error(f"The specified config file is invalid")
        raise SystemExit

else:
    logging.error("Invalid option")
    raise SystemExit(f"Usage {sys.argv[0]} (-c | -h) <arguments>...")

try:
    app = login(config['NAME']['BOT_NAME'], config['TOKENS']['API_ID'], config['TOKENS']['API_HASH'], config['TOKENS']['BOT_TOKEN'])
    app.run()
except (pyrogram.errors.ApiIdInvalid, pyrogram.errors.PhoneNumberInvalid) as e:
    logger.error(f"Error authenticating: {e.MESSAGE}.")
    raise SystemExit
