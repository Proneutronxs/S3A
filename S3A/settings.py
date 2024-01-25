"""
Django settings for S3A project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o@gi7gzjk8)i3m_gqsqu94$diq2^joa!8gr%1pi*td3e9bqi5_'

# SECURITY WARNING: don't run with debug turned on in production! ##
DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Applications.Mobile.GeneralApp',
    'Applications.Mobile.Anticipos',
    'Applications.Mobile.HorasExtras',
    'Applications.Mobile.FletesRemitos',
    'Applications.Mobile.Presentismo',
    'Applications.TareasProgramadas',
    'django_crontab',
    'Applications.TresAses',
    'Applications.RRHH',
    'Applications.Reportes',
    'Applications.Inicio',
    'Applications.Empaque',
    'Applications.Frio',
    'Applications.Logistica',
    'Applications.Bascula',
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

ROOT_URLCONF = 'S3A.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'S3A.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

###### ORIGINAL S3A
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'S3A/SQLite/db.SQLite',
#     },
#     'TRESASES_APLICATIVO': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'TRESASES_APLICATIVO',
#         'USER': 'sa',
#         'HOST': '192.168.1.3\sql2012',
#         'PASSWORD': '',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     },
#     'ISISPayroll': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'TresAses_ISISPayroll',
#         'USER': 'sa',
#         'HOST': '192.168.1.3\sql2012',
#         'PASSWORD': '',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     },
#     'principal': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'principal',
#         'USER': 'sa',
#         'HOST': '192.168.1.3\sql2012',
#         'PASSWORD': '',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     },
#     'S3A': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'S3A',
#         'USER': 'sa',
#         'HOST': '192.168.1.3\sql2012',
#         'PASSWORD': '',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'S3A/SQLite/db.SQLite',
#     },
# }


###### LOCAL S3A
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'S3A/SQLite/db.SQLite',
#     },
#     'TRESASES_APLICATIVO': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'TRESASES_APLICATIVO',
#         'USER': 'sa',
#         'HOST': '192.168.0.11',
#         'PASSWORD': 'Sideswipe348',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     },
#     'ISISPayroll': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'TresAses_ISISPayroll',
#         'USER': 'sa',
#         'HOST': '192.168.0.11',
#         'PASSWORD': 'Sideswipe348',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     },
#     'principal': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'principal',
#         'USER': 'sa',
#         'HOST': '192.168.0.11',
#         'PASSWORD': 'Sideswipe348',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     },
#     'S3A': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'S3A',
#         'USER': 'sa',
#         'HOST': '192.168.0.11',
#         'PASSWORD': 'Sideswipe348',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     }
# }

######FORWARDING
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'S3A/SQLite/db.SQLite',
    },
    'TRESASES_APLICATIVO': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'TRESASES_APLICATIVO',
        'USER': 'sa',
        'HOST': '186.127.54.205,20',
        'PASSWORD': 'Sideswipe348',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
    'ISISPayroll': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'TresAses_ISISPayroll',
        'USER': 'sa',
        'HOST': '186.127.54.205,20',
        'PASSWORD': 'Sideswipe348',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
    'principal': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'principal',
        'USER': 'sa',
        'HOST': '186.127.54.205,20',
        'PASSWORD': 'Sideswipe348',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
    'S3A': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'S3A',
        'USER': 'sa',
        'HOST': '186.127.54.205,20',
        'PASSWORD': 'Sideswipe348',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.tresases.com.ar'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aplicativo@tresases.com.ar'
EMAIL_HOST_PASSWORD = '8vzU&Uz3iorn'


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_FAILURE_VIEW = 'Applications.TresAses.views.error_403'
handler403 = 'Applications.TresAses.views.error_403'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

LOGOUT_REDIRECT_URL = reverse_lazy('tresases')

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

DATA_UPLOAD_MAX_MEMORY_SIZE = 50242880

CRONJOBS = [
    #('0 */2 * * *', 'Applications.TareasProgramadas.tasks.TrasladoLegajos') # EJECUTAR CADA DOS HORAS
    ################################## TRASPASO DE LEGAJOS DE ISIS A PRINCIPAL ################################## 
    ('0 */1 * * *', 'Applications.TareasProgramadas.tasks.TrasladoLegajos'), # EJECUTAR CADA UNA HORAS

    ################################## PROCESO DE HORAS EXTRAS ################################## 
    ('25,55 * * * *', 'Applications.TareasProgramadas.tasks.procesoHorasExtras'), # EJECUTAR CADA HORA A LOS 25 MIN y 55 MIN
    #('35 11,16 * * *', 'Applications.TareasProgramadas.tasks.TrasladoLegajos')# EJECUTAR TODOS LOS DIAS A LAS  12 Y 16 HS

    ('*/15 * * * *', 'Applications.TareasProgramadas.tasks.enviaCorreosAnticipos'),  # Ejecutar cada 5 minutos
    #('15 7 * * *', 'Applications.TareasProgramadas.tasks.sumar_numeros')  # Ejecutar a las 07:15
    ('20,50 * * * *', 'Applications.TareasProgramadas.tasks.procesa_arreglos'), # EJECUTAR CADA HORA A LOS 20 MIN y 50 MIN
]