from utils import get_translation

_ = get_translation()

START_MESSAGE = _(f"""
Hello! 👋

I'm a bot that will help you generate a working link to a news article or story from a blocked news site.

Send me the link you want to share.

""")

HELP_MESSAGE = _(f"""
This bot generates working links to news articles or stories from censored news sites.

Send the bot a link to an article from a blocked news site, and if the site is supported, it will send you back a working link.
""")

URL_ERR_MESSAGE = _("This news site is not yet supported")

REPORT_TRUE = _('Link will be reported.')

