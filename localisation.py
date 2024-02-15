import gettext

appname = 'SR2_bot'
localedir = './locales'

def setLanguage(language):
    gettext.translation(appname, localedir, fallback=True, languages=[language.strip()]).install()
