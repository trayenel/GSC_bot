from pyrogram.errors import ApiIdInvalid

from bot import app
from localisation import setLanguage

setLanguage("en")

try:
    app.run()
except ApiIdInvalid as e:
    print(e.MESSAGE)
