from configuration import logger
from pyrogram.errors import ApiIdInvalid
from bot import app


try:
    app.run()
except ApiIdInvalid as e:
    logger.error(f"Error authenticating: {e.MESSAGE}.")
    raise SystemExit
