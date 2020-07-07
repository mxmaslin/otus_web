import os

from configurations import Configuration
from dotenv import load_dotenv

load_dotenv()


class CommonSettings(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALLOWED_HOSTS = ['*']
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework_swagger',
        'graphene_django',
        'courses.apps.CoursesConfig',
        'profiles.apps.ProfilesConfig',
        'feedback.apps.FeedbackConfig',
        'debug_toolbar',
        'rest_framework',
        'knox',
        'corsheaders',
        'rest_framework.authtoken',
        'webpack_loader',
    ]
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    ROOT_URLCONF = 'coursera_react2.urls'
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    WSGI_APPLICATION = 'coursera_react2.wsgi.application'
    path = 'django.contrib.auth.password_validation'
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': f'{path}.UserAttributeSimilarityValidator'},
        {'NAME': f'{path}.MinimumLengthValidator'},
        {'NAME': f'{path}.CommonPasswordValidator'},
        {'NAME': f'{path}.NumericPasswordValidator'}
    ]
    LANGUAGE_CODE = 'en-us'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    TIME_ZONE = 'Europe/Moscow'
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
        os.path.join(BASE_DIR, 'src'),
    )
    AUTH_USER_MODEL = 'profiles.User'
    INTERNAL_IPS = ['127.0.0.1']
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'

    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = f'{BASE_DIR}/tmp/feedback'

    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
    CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    }
    GRAPHENE = {
        'SCHEMA': 'coursera_react2.schema.schema'
    }
    TEST_RUNNER = 'coursera_react2.runner.PytestTestRunner'
    DEBUG = True

    WEBPACK_LOADER = {
        'DEFAULT': {
            'CACHE': not DEBUG,
            'BUNDLE_DIR_NAME': 'dist/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
            'POLL_INTERVAL': 0.1,
            'TIMEOUT': None,
            'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
            'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
        }
    }
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
    SESSION_COOKIE_SAMESITE = None
    CSRF_COOKIE_SAMESITE = None


class Dev(CommonSettings):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(CommonSettings.BASE_DIR, 'db.sqlite3'),
        }
    }


class Prod(CommonSettings):
    pass
