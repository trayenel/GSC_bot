from helper_functions import validateUrl, setLanguage
from lang_constants import START_MESSAGE, HELP_MESSAGE
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import tldextract

def login(name, API_ID, API_HASH, BOT_TOKEN):
    app = Client(name, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


    @app.on_message(filters.command(["start"]) & filters.private)
    async def startHandler(client, message):
        await app.send_message(message.chat.id, _(START_MESSAGE))


    @app.on_message(filters.command(["help"]) & filters.private)
    async def helpHandler(client, message):
        await app.send_message(message.chat.id, _(HELP_MESSAGE))


    @app.on_message(filters.command(["lang"]) & filters.private)
    async def startHandler(client, message):
        await app.send_message(
            message.chat.id,
            "Lang",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🇷🇴", callback_data="ro"),
                        InlineKeyboardButton("🇷🇺", callback_data="ru"),
                        InlineKeyboardButton("🇬🇧", callback_data="en"),
                    ]
                ]
            ),
        )


    @app.on_callback_query()
    async def answer(client, callback_query):
        setLanguage(callback_query.data)


    @app.on_message(filters.private)
    async def domainHelper(client, message):
        if not validateUrl(message.text):
            await app.send_message(
                message.chat.id, "Unsupported site, select /help to see what this bot does."
            )
            return
        await app.send_message(
            message.chat.id, tldextract.extract(message.text).registered_domain
        )
    return app