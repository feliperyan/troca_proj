# Django settings for troca_proj project.
import os
import mongoengine
import re

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA_PATH = os.path.join(SITE_ROOT, '../media')
TEMPLATES_PATH = os.path.join(SITE_ROOT, 'templates')

MEDIA_ROOT = MEDIA_PATH 
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(SITE_ROOT, '../staticfiles')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

FACEBOOK_API_KEY = '112921768860216'
FACEBOOK_APP_ID = '112921768860216'
FACEBOOK_APP_SECRET = '32c7334cbf6811abdf6d8579e59c0cac'

AWS_ACCESS_KEY_ID = 'AKIAJQWT2VDXZR2OVOCA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'trocaeuitems'

if os.environ.has_key('AWS_ACCESS_KEY_ID'):
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = 'trocaeuitems'

    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    
    DEFAULT_S3_PATH = "media"
    STATIC_S3_PATH = "static"

    MEDIA_ROOT = '/media/'
    MEDIA_URL = '//s3.amazonaws.com/trocaeuitems/media/' 
    STATIC_ROOT = 'static'
    STATIC_URL = '//s3.amazonaws.com/trocaeuitems/static/' 
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

FACEBOOK_REGISTRATION_BACKEND = 'django_facebook.registration_backends.UserenaBackend'
AUTH_PROFILE_MODULE = 'troca_app.TrocaUserProfile'
ANONYMOUS_USER_ID = -1

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

# FELIPE: Dont use gravatar as I dont wanna send peoples email addresses
# unencrypted.
USERENA_MUGSHOT_GRAVATAR = False

MANAGERS = ADMINS

DBNAME = 'mongo_db'

# FELIPE: Handling either local MongoDB for dev or Heroku's MongoLab MongoDB.
regex = re.compile(r'^mongodb\:\/\/(?P<username>[_\w]+):(?P<password>[\w]+)@(?P<host>[\.\w]+):(?P<port>\d+)/(?P<database>[_\w]+)$')

if not os.environ.has_key('MONGOLAB_URI'):
    mongoengine.connect(DBNAME)
else:
    mongolab_url = os.environ['MONGOLAB_URI']
    match = regex.search(mongolab_url)
    data = match.groupdict()
    mongoengine.connect(data['database'], host=data['host'], port=int(data['port']), username=data['username'], password=data['password'])

# FELIPE: Heroku specific Database settings.
import dj_database_url
if not os.environ.has_key('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'postgres://localhost/troca_nonrel'
    
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'njbw-3ksmuhus4s9o=ezevc+mfle9vr&amp;e23x1yp9o-*-tizr$^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'troca_proj.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'troca_proj.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    TEMPLATES_PATH
)


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'troca_app',
    'userena',
    'guardian',
    'easy_thumbnails',
    'django_facebook',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
     'mongonaut',
     'storages',
     's3_folder_storage',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
]

# The next 2 lists are stuff added from django_facebook

#AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'
# NOTE: THIS PROFILE MODEL IS ACTUALLY IN MY OWN APP, I JUST NAMED IT
# LIKE THIS SO IT'D BE GROUPED WITH THE OTHER PROFILE STUFF!!!
#AUTH_PROFILE_MODULE = 'django_facebook.TrocaUserProfile'

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    #'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django_facebook.context_processors.facebook',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'        
        }
    },
    
    'loggers': {
        'troca': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}
