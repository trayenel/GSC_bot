import pyrogram.errors
import logging
import configparser
import asyncio
from pyrogram import idle
from bot import login
from helper_functions import init_argparse

loop = asyncio.get_event_loop()
logger = logging.getLogger("SR2_bot")
config = configparser.ConfigParser()
args = init_argparse().parse_args()

logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("root").setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

try:
    with open(args.file) as configFile:
        config.read(configFile.name)
except FileNotFoundError:
    logging.error(f"Config file not found.")
    raise SystemExit
except (configparser.MissingSectionHeaderError, configparser.NoOptionError):
    logging.error(f"The specified config file is invalid")
    raise SystemExit

try:
    logger.info("Application is starting.")
    asyncio.run(login(
        config["NAME"]["BOT_NAME"],
        config["TOKENS"]["API_ID"],
        config["TOKENS"]["API_HASH"],
        config["TOKENS"]["BOT_TOKEN"],
    ))
    logger.info("Application is starting.")

except (pyrogram.errors.ApiIdInvalid, pyrogram.errors.PhoneNumberInvalid) as e:
    logger.error(f"Error authenticating: {e.MESSAGE}.")
    raise SystemExit
