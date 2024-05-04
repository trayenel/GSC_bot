import logging
import requests

from database import upsertLink, upsertLang, selectLang, selectLink, session, Users
from utils import (
    validateUrl,
    extractUrl,
    available_locales,
    get_rows,
    get_translation, getUserLang
)
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
from urllib.parse import urlparse


async def login(name, API_ID, API_HASH, BOT_TOKEN):
    app = Client(name, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

    @app.on_message(filters.command(["start"]) & filters.private)
    async def startHandler(client, message):
        user_lang = getUserLang(message)

        upsertLang(Users, message.chat.id, user_lang)
        session.commit()

        locales = available_locales.keys()

        return await send_language_menu(client, message.chat.id, user_lang)

    @app.on_message(filters.command(["help"]) & filters.private)
    async def helpHandler(client, message):
        print(selectLink(Users, message.chat.id))
        # await app.send_message(message.chat.id, _(HELP_MESSAGE))

    @app.on_message(filters.private)
    async def domainHandler(client, message):

        try:
            _ = get_translation(selectLang(Users, message.chat.id))
        except Exception as e:
            logging.error(e)
            _ = get_translation()

        if not validateUrl(message.text):
            await app.send_message(
                message.chat.id,
                _(URL_ERR_MESSAGE),
            )
            return

        upsertLink(Users, message.chat.id, message.text)
        session.commit()

        link = 'https://' + extractUrl(message.text) + urlparse(message.text).path

        r = requests.get(f'http://redirector.cgdev.uk:5000/link?url={link}&type=getsitecopy')

        if r.status_code == 500:
            return await app.send_message(message.chat.id, _(URL_ERR_MESSAGE))

        res = r.json()
        return await app.send_message(message.chat.id, res["url"])

    async def send_language_menu(client: Client, chat_id: int, user_lang: str):
        # Set the translation to user_lang.
        _ = get_translation(user_lang)

        lang_rows = []
        locales = available_locales

        # The sort function is being used to reorder the list so user.language_code
        # is the first button, in a way to make it easier for the user to pick
        # their language if Telegram returned the correct one.
        for lang in sorted(locales, key=user_lang.__eq__, reverse=True):
            lang_rows.append(
                InlineKeyboardButton(
                    text=f'{locales[lang]["full_name"]} ({lang})',
                    callback_data=lang,
                )
            )

        button_rows = get_rows(lang_rows, 3)

        lang_markup = InlineKeyboardMarkup(button_rows)

        await client.send_message(
            chat_id=chat_id,
            text=_("Please select your language:"),
            reply_markup=lang_markup,
        )

    async def send_welcome_message(client: Client, user_id: int, lang: str):
        upsertLang(Users, user_id, lang)
        session.commit()

        _ = get_translation(lang)

        bot_name = _("GSC_Bot")

        # If lang is English, label = 'Change Language 🌐'
        # else label = "<'Change Language' translated> (Change Language) 🌐"

        if lang.startswith("en_") or lang == "en":
            change_lang_button_label = "Change Language 🌐"
        else:
            change_lang_button_label = _("Change Language") + " (Change Language) 🌐"

        await client.send_message(
            chat_id=user_id,
            text=_(START_MESSAGE),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            change_lang_button_label, "change_lang:" + lang
                        )
                    ], [InlineKeyboardButton(
                    _('Report'), "report:" + lang
                )]
                ]
            ),
        )

    async def send_report_menu(client, message, lang):
        _ = get_translation(lang)

        await app.send_message(
            message.chat.id,
            _(REPORT_MSG) + " " + selectLink(Users, message.chat.id) + " ?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(_("Yes"), "yes:" + lang),
                        InlineKeyboardButton(_("No"), "no:" + lang),
                    ]
                ]
            ),
            )

    @app.on_callback_query()
    async def answer(client, callback_query):
        if callback_query.data.split(':')[0] == "report":
            return await send_report_menu(client, callback_query.message, callback_query.data.split(':')[1])

        if callback_query.data.split(":")[0] == "yes":
            _ = get_translation(callback_query.data.split(':')[1])
            return await client.send_message(callback_query.from_user.id, _(REPORT_TRUE))

        if callback_query.data.split(":")[0] == "no":
            _ = get_translation(callback_query.data.split(':')[1])

            return await client.send_message(callback_query.from_user.id, _(REPORT_FALSE))

        if callback_query.data.split(":")[0] == "change_lang":
            return await send_language_menu(
                client,
                callback_query.message.chat.id,
                callback_query.data.split(":")[1],
            )

        return await send_welcome_message(
            client, callback_query.from_user.id, callback_query.data
        )

    await app.start()

    logging.getLogger("SR2_bot").info("Auth successful")

    await idle()

    session.close()

    await app.stop()
