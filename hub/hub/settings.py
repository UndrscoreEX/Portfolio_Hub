from pathlib import Path
import os
import boto3
from dotenv import load_dotenv
ssm = boto3.client('ssm',region_name='ap-northeast-1')
PARAMETER = ssm.get_parameter(Name='SECRET_KEY').get('Parameter').get('Value')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


AI_GEN_TEMPLATE_DIR = BASE_DIR / 'ai_gen/templates/ai_image_gen'

#
# only for dev
STATICFILES_DIRS = [
    BASE_DIR / "ai_gen" /"static",
]
print(STATICFILES_DIRS)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#
#

S3_PREFIX = "https://portfolio-items-underscore-ex.s3.ap-northeast-1.amazonaws.com"
CLOUDFRONT_PREFIX = "https://d38261ux8dbby0.cloudfront.net"

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = PARAMETER

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("SYSTEM") == 'dev'

ALLOWED_HOSTS = ['localhost','127.0.0.1','18.176.194.245', 'underscore-ex.com', 'www.underscore-ex.com', '0.0.0.0','www.google.com']


# Application definition
INSTALLED_APPS = [
    'channels',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    "django_browser_reload",
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware'
    'ai_gen',
    'bach_calc',
    'portfolio',
    "stock",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'hub.context_processors.cloudfront_prefix'
            ],
        },
    },
]

WSGI_APPLICATION = 'hub.wsgi.application'
CSRF_TRUSTED_ORIGINS = [
    'https://www.underscore-ex.com',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1200  # 20 minutes


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
ASGI_APPLICATION = 'hub.asgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# S3_MEDIA_ROOT = 'https://portfolio-items-underscore-ex.s3.ap-northeast-1.amazonaws.com/PortfolioApp/'
# S3_URL_PREFIX = 'static/'

STATICFILES_DIRS = [
    # BASE_DIR / "bach_calc/static",
    # BASE_DIR / "portfolio/static/portfolio",
    # BASE_DIR / "ai_gen/static",
    BASE_DIR / "static"
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
