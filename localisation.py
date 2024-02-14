import gettext
appname = 'SR2_bot'
localedir = './locales'

i18n = gettext.translation(appname, localedir, fallback=True, languages=['en', 'ro'])
