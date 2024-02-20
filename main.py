import logging
from pyrogram.errors import ApiIdInvalid
from bot import app


try:
    app.run()
except ApiIdInvalid as e:
    logging.error(f"Error authenticating: {e.MESSAGE}.")
    raise SystemExit
