import validators
import gettext
import argparse

appname = "SR2_bot"
localedir = "./locales"


def setLanguage(language):
    gettext.translation(
        appname, localedir, fallback=True, languages=[language.strip()]
    ).install()


def validateUrl(url):
    if validators.domain(url) or validators.url(url):
        return True
    return False


def init_argparse() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        usage="%(prog)s -c [FILE]",
        description="Start telegram bot.",
    )
    parser.add_argument("filename")
    return parser
