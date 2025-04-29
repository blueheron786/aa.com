import datetime

AUTHOR = 'Ashiq Alibhai'
SITENAME = 'Ashiq Alibhai, Author of Fantasy & Sci-Fi'
SITESUBTITLE = 'Exploring Faith, Imagination, and Distant Worlds'
SITEURL = "localhost:8000"

PATH = "content"

# Content sources
ARTICLE_PATHS = ['articles', 'books']   # normal blog posts
PAGE_PATHS = ['pages']          # standalone pages like About
STATIC_PATHS = ['images']

# URL configz
ARTICLE_URL = '{category}/{slug}.html'
ARTICLE_SAVE_AS = '{category}/{slug}.html'

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# General configz
TIMEZONE = 'America/Toronto'
DEFAULT_LANG = 'en'
THEME = 'themes/flexing'
INDEX_SAVE_AS = 'blog/index.html'
#DIRECT_TEMPLATES = ['blog']  # NOT 'index'
DEFAULT_ORDER = 'by-date'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['home_content_injector']

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