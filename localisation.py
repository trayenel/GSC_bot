# Import gettext module
import gettext

# Set the local directory
appname = 'SR2_bot'
localedir = './locales'

# Set up Gettext
en_i18n = gettext.translation(appname, localedir, fallback=True, languages=['en'])

# Create the "magic" function
en_i18n.install()

# Translate message
print(gettext.gettext("Hello World"))