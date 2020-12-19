from .base import *
import psycopg2

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': os.getenv("USER"),
        'PASSWORD': os.getenv("PASSWORD"),
        'NAME': os.getenv("NAME"),
        'HOST': os.getenv("HOST"),
        'PORT': '5432',
    }
}

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# DATABASES['default'] = dj_database_url.config(
#     conn_max_age=600, ssl_require=True)
