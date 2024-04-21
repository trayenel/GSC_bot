import logging
from database import upsertLink, selectLink, session, Links
from utils import validateUrl, setLanguage, extractUrl, available_locales, get_translation, get_rows
from lang_constants import (
    START_MESSAGE,
    HELP_MESSAGE,
    URL_ERR_MESSAGE,
    REPORT_TRUE,
    REPORT_FALSE,
    REPORT_MSG,
)
from pyrogram import Client, filters, idle
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

async def login(name, API_ID, API_HASH, BOT_TOKEN):
    app = Client(name, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

    @app.on_message(filters.command(["report"]) & filters.private)
    async def reportLink(client, message):
        await app.send_message(
            message.chat.id,
            _(REPORT_MSG) + " " + selectLink(Links, message.chat.id) + " ?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(_('Yes'), callback_data="yes"),
                        InlineKeyboardButton(_('No'), callback_data="no"),
                    ]
                ]
            ),
            )

    @app.on_callback_query()
    async def answer(client, callback_query):
        if callback_query.data == "yes":
            await callback_query.answer(_(REPORT_TRUE), show_alert=True)

            return
        if callback_query.data == "no":
            await callback_query.answer(_(REPORT_FALSE), show_alert=True)
        setLanguage(callback_query.data)
        return

    @app.on_message(filters.command(["start"]) & filters.private)
    async def startHandler(client, message):
        user = message.from_user
        if not user:
            return None

        user_lang = user.language_code
        if user_lang is None:
            user_lang = "en"
        else:
            user_lang = user_lang.lower()

        locales = available_locales.keys()

        if user_lang != "en" and user_lang in locales:
            return await send_welcome_message(client, message.from_user.id, user_lang)

        await send_language_menu(client, message.chat.id, user_lang)

    @app.on_message(filters.command(["help"]) & filters.private)
    async def helpHandler(client, message):
        await app.send_message(message.chat.id, _(HELP_MESSAGE))

    @app.on_message(filters.private)
    async def domainHandler(client, message):
        if not validateUrl(message.text):
            await app.send_message(
                message.chat.id,
                _(URL_ERR_MESSAGE),
            )
            return
        upsertLink(Links, message.chat.id, message.text)
        session.commit()
        await app.send_message(message.chat.id, extractUrl(message.text))

    await app.start()

    logging.getLogger("SR2_bot").info("Auth successful")

    await idle()

    session.close()

    await app.stop()
