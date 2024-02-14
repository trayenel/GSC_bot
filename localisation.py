import gettext

appname = 'SR2_bot'
localedir = './locales'

gettext.translation(appname, localedir, fallback=True, languages=['en']).install()

print(_("Hello World"))