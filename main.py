from localisation import *
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

i18n.install()

app = Client("botTest", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command(["start"]) & filters.private)
async def startHandler(client, message):
    await app.send_message(message.chat.id, "Salutare, pentru ajutor tastati tasta /help")


@app.on_message(filters.command(["help"]) & filters.private)
async def helpHandler(client, message):
    await app.send_message(message.chat.id, "Pentru menu tastatzi /menu")


@app.on_message(filters.command(["menu"]) & filters.private)
async def menuHandler(client, message):
    await app.send_message(
        message.chat.id,
        "Cine este cel mai misto MANELIST?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Florin Salam",
                        url="https://youtu.be/-KBTMvlziBk?feature=shared&t=49",
                    ),
                    InlineKeyboardButton("Nicolae guta", url="www.mata.com"),
                ],
                [
                    InlineKeyboardButton("Tzanca Uraganu", url="www.mata.com"),
                    InlineKeyboardButton("Copilu de Aur", url="www.mata.com"),
                ],
            ]
        ),
    )


app.run()
