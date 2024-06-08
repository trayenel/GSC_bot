import logging
import requests
import validators

from database import (
    upsertLink,
    upsertLang,
    selectLang,
    selectLink,
    selectReport,
    upsertReport,
    addUser,
    session,
    Chats,
)
from utils import available_locales, get_rows, get_translation, getUserLang
from lang_constants import (
    START_MESSAGE,
    HELP_MESSAGE,
    SITE_UNSUPPORTED_MESSAGE,
    REPORT_TRUE,
    BROKEN_URL_MESSAGE
)
from pyrogram import Client, filters, idle
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


async def login(name, API_ID, API_HASH, BOT_TOKEN):
    app = Client(name, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

    @app.on_message(filters.command(["start"]) & filters.private)
    async def startHandler(client, message):
        try:
            logging.getLogger('gsc-bot').info(f'Getting chat id {message.chat.id} stored language.')
            user_lang = selectLang(Chats, message.chat.id)
            logging.getLogger('gsc-bot').info(f"User's lang is set to: {user_lang}.")
        except:
            logging.getLogger('gsc-bot').error(f'Chat id {message.chat.id} not yet in database.')
            user_lang = getUserLang(message)
            logging.getLogger('gsc-bot').info(f'Using chat id app language: {message.from_user.language_code}')

        locales = available_locales.keys()

        return await send_language_menu(client, message.chat.id, user_lang)

    @app.on_message(filters.command(["help"]) & filters.private)
    async def helpHandler(client, message):
        try:
            user_lang = selectLang(Chats, message.chat.id)
        except:
            logging.getLogger('gsc-bot').info(f"Chat id {message.chat.id} did not select language. Using app lang.")
            user_lang = message.from_user.language_code
            addUser(Chats, message.chat.id)
            session.commit()
            logging.getLogger('gsc-bot').info(f"Chat id {message.chat.id} added to database.")

        _ = get_translation(user_lang)

        await app.send_message(message.chat.id, _(HELP_MESSAGE))

    @app.on_message(filters.private)
    async def domainHandler(client, message):
        try:
            user_lang = selectLang(Chats, message.chat.id)
        except:
            logging.getLogger('gsc-bot').info(f"Chat id {message.chat.id} did not select language. Using app lang.")
            user_lang = message.from_user.language_code
            addUser(Chats, message.chat.id)
            session.commit()
            logging.getLogger('gsc-bot').info(f"Chat id {message.chat.id} added to database.")

        _ = get_translation(user_lang)

        if not validators.url(message.text):
            await app.send_message(
                message.chat.id,
                _(HELP_MESSAGE),
            )
            return

        storedLink = selectLink(Chats, message.chat.id)
        if storedLink != message.text:
            logging.getLogger("gsc-bot").info(
                f"Storing link from chat id {message.chat.id} in database: {message.text}")
            upsertLink(Chats, message.chat.id, message.text)
            upsertReport(Chats, message.chat.id, 0)
            session.commit()
            logging.getLogger("gsc-bot").info(f"Link from chat id {message.chat.id} stored.")

        link = message.text

        redirector_request = f"http://redirector.cgdev.uk:5000/link?url={link}&type=getsitecopy"

        logging.getLogger("gsc-bot").info(
            f"Requesting link from chat id {message.chat.id} to redirector: {message.text}")

        r = requests.get(redirector_request)

        if r.status_code == 403:
            await send_link_with_report_menu(
                client, message.chat.id, user_lang, _(SITE_UNSUPPORTED_MESSAGE)
            )
            return logging.getLogger("gsc-bot").error(f"Link from chat id {message.chat.id} unsupported by redirector.")

        if r.status_code == 500:
            await send_link_with_report_menu(
                client, message.chat.id, user_lang, _(BROKEN_URL_MESSAGE))
            return logging.getLogger("gsc-bot").error(f"Link from chat id {message.chat.id} is broken.")

        url = r.json()["url"]

        if url is not None:
            await send_link_with_report_menu(client, message.chat.id, user_lang, url)

            return logging.getLogger("gsc-bot").info(
                f"Link from chat id {message.chat.id} successfully fetched: {redirector_request}")

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

    async def send_link_with_report_menu(
            client: Client, user_id: int, lang: str, textStr: str
    ):
        _ = get_translation(lang)

        await client.send_message(
            chat_id=user_id,
            text=textStr,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(_("Report broken link"), "report:" + lang)]]
            ),
        )

    async def send_welcome_menu(client: Client, user_id: int, lang: str):
        logging.getLogger('gsc-bot').info(f'Chat id {user_id} changed language to {lang}.')
        upsertLang(Chats, user_id, lang)
        session.commit()

        _ = get_translation(lang)

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
                    ],
                ]
            ),
        )
        return

    @app.on_callback_query()
    async def answer(client, callback_query):
        if callback_query.data.split(":")[0] == "report":
            _ = get_translation(callback_query.data.split(":")[1])

            logging.getLogger("gsc-bot").info(
                f"Chat id {callback_query.from_user.id} reporting link: {selectLink(Chats, callback_query.from_user.id)}")

            if selectReport(Chats, callback_query.from_user.id) == 1:
                await client.send_message(
                    callback_query.from_user.id, _("Link already reported")
                )
                return logging.getLogger("gsc-bot").error(f"Link already reported.")

            upsertReport(Chats, callback_query.from_user.id, 1)
            logging.getLogger("gsc-bot").info(f"Link reported by chat id: {callback_query.from_user.id}.")

            return await client.send_message(
                callback_query.from_user.id, _(REPORT_TRUE)
            )

        if callback_query.data.split(":")[0] == "change_lang":
            return await send_language_menu(
                client,
                callback_query.message.chat.id,
                callback_query.data.split(":")[1],
            )

        return await send_welcome_menu(
            client, callback_query.from_user.id, callback_query.data
        )

    logging.getLogger("gsc-bot").info("Auth successful")

    await app.start()

    logging.getLogger("gsc-bot").info("App started")

    await idle()

    session.close()

    await app.stop()
