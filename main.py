from pyrogram import Client
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

API_ID = 29981079
API_HASH = "dfd1afdf1799bb2581292557762cf223"
BOT_TOKEN = "6413043221:AAG5xn797fReEmtx_hsMZEbfXNcOpaPb4FU"

start_msg = "Salutare, pentru ajutor tastati tasta /help"
help_msg = "Pentru menu tastatzi /menu"
menu_msg = "Cine este cel mai misto manelist?"

app = Client("botTest", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command(["start"]) & filters.private)
async def startHandler(client, message):
    await app.send_message(message.chat.id, start_msg)


@app.on_message(filters.command(["help"]) & filters.private)
async def helpHandler(client, message):
    await app.send_message(message.chat.id, help_msg)


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
