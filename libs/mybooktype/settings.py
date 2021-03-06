import os.path

# DJANGO DEBUG
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# DJANGO ADMIN
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DEFAULT_NOTIFICATION_FILTER=u"#* !* ~* \u212c*"

# You can customize which publish options this installation can use.
# Options are: book, ebook, pdf, lulu, odt
# PUBLISH_OPTIONS = ("book", "ebook")

# BOOKI
BOOKI_MAINTENANCE_MODE = False

BOOKI_NAME = 'Booki site'
THIS_BOOKI_SERVER = '' # the name of the booki server (comment out to use os.environ['HTTP_HOST'])

BOOKI_ROOT = os.path.dirname(__file__)  # edit this
BOOKI_URL = ''
#BOOKI_URL = 'http://%s' % THIS_BOOKI_SERVER

# E-MAIL OPTIONS
REPORT_EMAIL_USER = 'booki@booki.cc'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
#EMAIL_HOST_USER = 'booki@' + THIS_BOOKI_SERVER
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = False

# BOOKI DIRECTORIES

# site_static
import booki

SITE_STATIC_ROOT = '%s/site_static' % os.path.dirname(booki.__file__)
SITE_STATIC_URL  = '%s/site_static' % BOOKI_URL

# static
STATIC_ROOT = '%s/static' % BOOKI_ROOT
STATIC_URL  = '%s/static' % BOOKI_URL

# data
DATA_ROOT = '%s/data' % BOOKI_ROOT
DATA_URL  = '%s/data' % BOOKI_URL

# profile images
PROFILE_IMAGE_UPLOAD_DIR = 'profile_images/' 

# If you don't want to use default profile image you can set your own.
# Place the image inside of /static/images/ directory in your Booktype project directory.
#DEFAULT_PROFILE_IMAGE='anonymous.jpg'

# book cover images			 
COVER_IMAGE_UPLOAD_DIR = 'cover_images/'

# obsolete
MEDIA_ROOT = DATA_ROOT
MEDIA_URL = DATA_URL

ADMIN_MEDIA_PREFIX = '%s/media/' % BOOKI_URL

# URLS
OBJAVI_URL = "http://objavi.booki.cc/objavi.cgi"
ESPRI_URL = "http://objavi.booki.cc/espri.cgi"
TWIKI_GATEWAY_URL = "http://objavi.booki.cc/booki-twiki-gateway.cgi"

# lulu.com export credentials that override Objavi settings
LULU_USER = None
LULU_PASSWORD = None
LULU_API_KEY = None

# who gets credited as publisher if not otherwise specified
DEFAULT_PUBLISHER = "Unknown"

# DATABASE STUFF
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': '%s/database.sqlite' % BOOKI_ROOT,
                         'USER': '',
                         'PASSWORD': '',
                         'HOST': 'localhost',
                         'PORT': ''
                        }
            }


# REDIS STUFF
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

# DJANGO STUFF

AUTH_PROFILE_MODULE='account.UserProfile'

TIME_ZONE = 'Europe/Berlin'

LANGUAGE_CODE = 'en-us'

# Uncomment this if you want to limit language translations only to specific list of languages
#
# gettext = lambda s: s
#
# LANGUAGES = (
#  ('en-us', gettext('English'))
# )

SITE_ID = 1

USE_I18N = True
USE_L10N = True

LOCALE_PATHS = (
     '%s/locale' % os.path.dirname(booki.__file__),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'enc*ln*vp^o2p1p6of8ip9v5_tt6r#fh2-!-@pl0ur^6ul6e)l'

# Storage for messages framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage' 

# List of callables that know how to import templates from various sources.
import django

if django.VERSION[1] < 3:
    TEMPLATE_LOADERS = (
                        'django.template.loaders.filesystem.load_template_source',
                        'django.template.loaders.app_directories.load_template_source',
                        'django.template.loaders.eggs.load_template_source',
                       )
else:
    TEMPLATE_LOADERS = (
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                        'django.template.loaders.eggs.Loader',
                       )

TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 
                               'django.contrib.messages.context_processors.messages') 

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'booki.urls'

TEMPLATE_DIRS = (
    '%s/templates/' % BOOKI_ROOT,
    '%s/templates/' % os.path.dirname(booki.__file__)
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages', 

    'south',

    # list of booki apps
    'booki.editor',
    'booki.account',
    'booki.reader',
    'booki.portal',
    'booki.messaging',

    'sputnik',
    'booktypecontrol'
)

# import openshift specific settings
from mybooktype.settings_openshift import *

# LOGGING

def init_logging():
    import logging
    import logging.handlers

    logger = logging.getLogger("booki")
    logger.setLevel(logging.DEBUG)
    ch = logging.handlers.RotatingFileHandler('%s/booki.log' % OPENSHIFT_LOG_DIR, maxBytes=100000, backupCount=5)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(ch)

logInitDone=False

if not logInitDone:
    logInitDone = True
    init_logging()

from booki.utils import config

try:
    BOOKTYPE_CONFIG = config.loadConfiguration()
except config.ConfigurationError:
    BOOKTYPE_CONFIG = {}
