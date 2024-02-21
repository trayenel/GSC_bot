import validators
import gettext

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

