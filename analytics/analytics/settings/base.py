import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'taggit',
    'django_quill',
    'django_countries',
    # 'social_django',
    'corsheaders',
    'django_hosts',
    'ckeditor',
    'ckeditor_uploader',

    'apps.accounts',
    'apps.analysis',
    'apps.shop',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',        # for per site cache
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',     # for per site cache
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'analytics.urls'

# For django_hosts
ROOT_HOSTCONF = 'analytics.hosts'

DEFAULT_HOST = 'www'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,
                os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'social_django.context_processors.backends',
                # 'social_django.context_processors.login_redirect',
                # 'cart.context_processor.cart_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'analytics.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'apadana.sqlite3'),
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
                    }
    }
}

# Using django memcache for caching
"""
CACHES = {
    'default': {
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 600                                        # cache never expires
    }
}
"""

# for cache per site:

# CACHE_MIDDLEWARE_ALIAS = 'apadana_cache'

# CACHE_MIDDLEWARE_SECONDS = 900

# CACHE_MIDDLEWARE_KEY_PREFIX = 'mem'

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

# AUTH_USER_MODEL = 'user.User'
AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = ','

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
# To deploy on Host (Sub folders do not accepted by host!):
# STATIC_ROOT = '/home/<serivce_name>/public_html/static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR),
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# To deploy on Host:
# MEDIA_ROOT = '/home/<serivce_name>/public_html/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login and Logout urls

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/login/'

LOGOUT_REDIRECT_URL = '/'

# We can also use 'reverse_lazy' to handle login and logout urls

# TAGGIT_CASE_INSENSITIVE = True

# Django social authentication settings:

# SOCIAL_AUTH_POSTGRES_JSONFIELD = True     <==> This is soon to be decapitated
# SOCIAL_AUTH_JSONFIELD_ENABLED = True

"""
AUTHENTICATION_BACKENDS = (
    # google oauth2 backend
    'social_core.backends.google.GoogleOAuth2',

    # normal django auth backend
    'django.contrib.auth.backends.ModelBackend',
)
"""

# ID_KEY and SECRET for google
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '696613813066-qi854fm95mv3h7meen44rbqgcel48mbu.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'KM1oanQONJYFvgtT9BVGu9gy'

# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [...]

# SOCIAL_AUTH_URL_NAMESPACE = 'social'    # It's optional, to make a default namespace for our social auth backend

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}

# Cors headers settings
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_ALL_ORIGINS = True

# CKEditor settings
# CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_BASEPATH = f"{STATIC_URL}ckeditor/ckeditor/"
# CKEDITOR_BASEPATH = (os.path.join(STATIC_URL, 'ckeditor', 'ckeditor', '')).replace("\\", "/")

CKEDITOR_UPLOAD_PATH = "uploads/"

# CKEditor optional settings
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        # 'toolbar': 'basic',
        # 'height': 300,
        # 'width': 300,
    },
}
