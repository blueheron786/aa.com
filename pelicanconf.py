import datetime

AUTHOR = 'Ashiq Alibhai'
SITENAME = 'Ashiq Alibhai, Author of Fantasy & Sci-Fi'
SITESUBTITLE = 'Exploring Faith, Imagination, and Distant Worlds'
SITEURL = "https://ashiqalibhai.com"

PATH = "content"

TIMEZONE = 'America/Toronto'

DEFAULT_LANG = 'en'
THEME = 'themes/flexing'

STATIC_PATHS = ['images', 'pdfs', 'extra']

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
)

# Social widget
SOCIAL = (
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

COPYRIGHT_YEAR = datetime.datetime.now().year
COPYRIGHT_NAME = AUTHOR
# Force dark mode. MY EYES!
THEME_COLOR = "dark"