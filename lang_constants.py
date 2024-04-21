from utils import setLanguage

setLanguage('en')

START_MESSAGE = _(f"""
Hello! 👋

I'm a bot that will help you generate a working link to a news article or story from a blocked news site.

Send me the link you want to share.

""")

HELP_MESSAGE = _(f"""
This bot is designed to allow you to freely share links from media sites blocked in Russia.

To get a working link to an article or news story, send the bot a link to an article from one of the blocked media sites or select Report to report a broken link.

""")

URL_ERR_MESSAGE = _("Unsupported site, select /help to see what this bot does.")

REPORT_TRUE = _('Link will be reported.')

REPORT_FALSE = _('Link will not be reported.')

REPORT_MSG = _(f"Do you want to report the following link:")
