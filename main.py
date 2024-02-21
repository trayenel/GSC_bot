import pyrogram.errors
import logging
import configparser
from bot import login
from helper_functions import init_argparse


config = configparser.ConfigParser()
logger = logging.getLogger("SR2_bot")
args = init_argparse().parse_args()

try:
    with open(args.file) as configFile:
        config.read(configFile.name)
except FileNotFoundError:
    logging.error("Config file not found.")
    raise SystemExit
except (configparser.MissingSectionHeaderError, configparser.NoOptionError):
    logging.error(f"The specified config file is invalid")
    raise SystemExit

try:
    login(
        config["NAME"]["BOT_NAME"],
        config["TOKENS"]["API_ID"],
        config["TOKENS"]["API_HASH"],
        config["TOKENS"]["BOT_TOKEN"],
    ).run()
except (pyrogram.errors.ApiIdInvalid, pyrogram.errors.PhoneNumberInvalid) as e:
    logger.error(f"Error authenticating: {e.MESSAGE}.")
    raise SystemExit
