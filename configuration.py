import configparser
import logging
import sys
import validators
import gettext

appname = "SR2_bot"
localedir = "./locales"

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

logger = logging.getLogger('SR2_bot')

def validateUrl(url):
    if validators.domain(url) or validators.url(url):
        return True
    return False


config = configparser.ConfigParser()
file = None

if "-h" in opts:
    print(f"Usage: {sys.argv[0]} [OPTIONS]")
    print(f"-c, --config FILE".ljust(20, " "), f"Specify a configuration file.")
    print(f"-h, --help".ljust(20, " "), f"Show this help message and exit.")

    raise SystemExit
elif "-c" in opts:
    try:
        file = open(args[-1], "r")
        config.read(file.name)
    except (FileNotFoundError, IndexError):
        logging.error("Config file not found.")
        raise SystemExit
    except (configparser.MissingSectionHeaderError, configparser.NoOptionError):
        logging.error(f"The specified config file is invalid")
        raise SystemExit

else:
    logging.error('Invalid option')
    raise SystemExit(f"Usage {sys.argv[0]} (-c | -h) <arguments>...")

API_ID = config["TOKENS"]["api_id"]
API_HASH = config["TOKENS"]["api_hash"]
BOT_TOKEN = config["TOKENS"]["bot_token"]
BOT_NAME = config["NAME"]["bot_name"]

def setLanguage(language):
    gettext.translation(
        appname, localedir, fallback=True, languages=[language.strip()]
    ).install()

setLanguage('en')

START_MESSAGE = _(f"""
Привет! 👋

Я бот, который поможет вам сгенерировать рабочую ссылку на новость или статью с сайта заблокированного СМИ.

Отправьте мне ссылку, которой хотите поделиться.
""" )  # noqa: E501

HELP_MESSAGE = _(f"""
Данный бот создан для того, чтобы вы могли безпрепятственно делиться ссылками с заблокированных в России сайтов СМИ.

Чтобы получить рабочую ссылку на статью или новость, отправьте боту ссылку на статью с одного из сайтов заблокированного СМИ.

""" )