
from BLOG.custom_login.config import LOGIN_MESSAGE, LOGIN_MESSAGE_CATEGORY, REFRESH_MESSAGE, REFRESH_MESSAGE_CATEGORY
import os

konfigdir = os.path.abspath(os.path.dirname(__file__))  # hvor vi legger DB

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    #FLASK_APP = "/BLOG/"  # oppgitt i launch.json, oppgitt i .env
    FLASK_ENV = "development"  # oppgitt i launh.json  oppgitt i .env
    LOG_AKTIV=True ## error logger
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'pbkdf2:sha256:150000$nb5qgXSe$1555dcc3976e10663dfb6e444329f589a34aef7fd1e21f2c26a8efc5c98897f6'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False ########### <------ SENKER YTELSE IF TRUE
    # DEBUG = True
    TESTING = True      # noe error handling som ellers ikke vises vil nå vises om 'True'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(konfigdir, "blog.db")
    SESSION_COOKIE_NAME = "CookieBlog"
    SQLALCHEMY_POOL_RECYCLE = 299  # etter 299 sek uten aktivitet brytes connect
    SQLALCHEMY_ECHO = True  # Alt til-fra db vises i konsoll for debug formål
    STATIC_FOLDER = "static"  # default=static
    #TEMPLATES_FOLDER = "templates"  # default=templates
    POST_PER_PAGE = 2
    COMMENTS_PER_PAGE = 3
    RECAPTCHA_PUBLIC_KEY="micromanagingtesting1223"
    RECAPTCHA_PRIVATE_KEY="testing123micromanagingexploringdoringchoring"
    ### login man: flyttes til __init; dette er ikke verdier som egentlig skal endres på.
    LOGIN_MESSAGE = "innlogging kreves."
    LOGIN_MESSAGE_CATEGORY = "messages"
    REFRESH_MESSAGE = "Re-autorisering kreves."
    REFRESH_MESSAGE_CATEGORY = "messages"
    REFRESH_VIEW = "main.index"  # her eller i _init_?

    print("Lastet konfig.")


# Kontroll.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'

# FLASK_APP='/BLOG/'  # oppgitt i launch.json, oppgitt i .env
# #FLASK_ENV='development' # oppgitt i launh.json  oppgitt i .env
# SECRET_KEY = 'gjett3ganger3ganger3'   #oppgitt i .env
# #DEBUG = True
# #TESTING = True      # noe error handling som ellers ikke vises vil nå vises om 'True'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(konfigdir, 'blog.db')
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SESSION_COOKIE_NAME = 'CookieBlog'
# SQLALCHEMY_POOL_RECYCLE = 299 # etter 299 sek uten aktivitet brytes connect
# SQLALCHEMY_ECHO = True        # Alt til-fra db vises i konsoll for debug formål
# STATIC_FOLDER = 'static'       # default=static
# TEMPLATES_FOLDER = 'templates'  # default=templates
