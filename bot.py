import logging
from database import upsertLink, selectLink, session, Links
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


async def login(name, API_ID, API_HASH, BOT_TOKEN):
    app = Client(name, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

    async def reportLink(client, message, lang):
        _ = get_translation(lang)

        await app.send_message(
            message.chat.id,
            _(REPORT_MSG) + " " + selectLink(Links, message.chat.id) + " ?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(_("Yes"), "yes:" + lang),
                        InlineKeyboardButton(_("No"), "no:" + lang),
                    ]
                ]
            ),
            )

    @app.on_message(filters.command(["start"]) & filters.private)
    async def startHandler(client, message):
        user_lang = getUserLang(message)

        locales = available_locales.keys()

        return await send_language_menu(client, message.chat.id, user_lang)

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

    @app.on_callback_query()
    async def answer(client, callback_query):
        if callback_query.data.split(':')[0] == "report":
            return await reportLink(client, callback_query.message, callback_query.data.split(':')[1])

        if callback_query.data.split(":")[0] == "yes":
            _ = get_translation(callback_query.data.split(':')[1])
            return await callback_query.answer(_(REPORT_TRUE), show_alert=True)

        if callback_query.data.split(":")[0] == "no":
            _ = get_translation(callback_query.data.split(':')[1])
            return await callback_query.answer(_(REPORT_FALSE), show_alert=True)

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
