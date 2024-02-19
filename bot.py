from configuration import (API_ID,
API_HASH,
BOT_TOKEN)
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import tldextract

app = Client("botTest", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command(["start"]) & filters.private)
async def startHandler(client, message):
    await app.send_message(
        message.chat.id,
        "Lang",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Romanian", callback_data="ro"),
                    InlineKeyboardButton("English", callback_data="en"),
                ]
            ]
        ),
    )


@app.on_callback_query()
async def answer(client, callback_query):
    setLanguage(callback_query.data)


@app.on_message(filters.command(["help"]) & filters.private)
async def helpHandler(client, message):
    await app.send_message(message.chat.id, _("Mamaliga cu mititei infasetei"))

@app.on_message(filters.private)
async def domainHelper(client, message):
    await app.send_message(message.chat.id, tldextract.extract(message.text).registered_domain)