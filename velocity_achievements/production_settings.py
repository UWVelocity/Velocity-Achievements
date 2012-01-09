from server_settings import *
import os.path

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.expanduser("~/velocity_achievements/production/media")

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.expanduser('~/velocity_achievements/production/static/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'velocity_achievements_production',
        'USER': 'velocity',
        'PASSWORD': 'f[1kS0122d',
        'HOST': '',
        'PORT': '',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'p*bpbz7#m7f^nevamw+rm&j=2t=ri7lk&p!-h85j6ojk132za3'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'debug.log'
        },
        
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'level': 'ERROR',
            'handlers': ['file'],
            'propagate': True,
        },
    },
}
