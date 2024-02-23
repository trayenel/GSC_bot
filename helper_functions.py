import validators
import gettext
import argparse
import tldextract


def setLanguage(language):
    gettext.translation(
        "SR2_bot", "./locales", fallback=True, languages=[language.strip()]
    ).install()


def validateUrl(url):
    if validators.domain(url) or validators.url(url):
        return True
    return False


def extractUrl(url):
    return tldextract.extract(url).registered_domain


def init_argparse() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        usage="%(prog)s -c [FILE]",
        description="Start telegram bot.",
    )
    parser.add_argument("file")
    parser.add_argument(
        "-c",
        "--config",
        action="store_true",
        help="load configuration file",
        required=True,
    )
    return parser
