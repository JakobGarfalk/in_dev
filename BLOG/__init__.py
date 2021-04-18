from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
from logging.handlers import RotatingFileHandler
import logging

from BLOG.custom_login import LoginManager
from config import Config ## .env fil leses i config.py
#from BLOG.functions.crapper.crapper import Crapper

db = SQLAlchemy()  # done here so that db is importable
migrate = Migrate()
login_man=LoginManager()
#crapper = Crapper()

def create_app(config_class=Config):
    app = Flask(__name__)               #
    app.config.from_object(config_class)#
    db.init_app(app)                    #
    migrate.init_app(app, db)           #
    #crapper.init_app(app, db)       # crapper tjener ingen hensikt. Det er en test case foreløpig.
    #register blueprints, configure logging etc.
    login_man.init_app(app)
    login_man.login_view="users.login_view" # hvor mange endringer før du flytter denne? ii
    
    from BLOG.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    # from BLOG.main import IndexView
    # app.add_url_rule("/", view_func=IndexView.as_view("index"))

    # from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')

    from BLOG.main import bp as main_bp
    app.register_blueprint(main_bp)
    from BLOG.Users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix="/bruker")

    if app.config["LOG_AKTIV"]==True:
    #if not app.debug:
        if not os.path.exists('logs'): os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/blog.log', maxBytes=10240,backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        ### logging.INFO ; DEBUG, INFO, WARNING, ERROR, CRITICAL =grad av hvor mye som logges
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('create app startup')
   
    return app
from BLOG.main import models
    # db.init_app(app)
    # migrate.init_app(app, db)
    # login.init_app(app)
    # mail.init_app(app)
    # bootstrap.init_app(app)
    # moment.init_app(app)
    # babel.init_app(app)

    # from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')

    # from app.main import bp as main_bp
    # app.register_blueprint(main_bp)
## dette må gjøres i view, eller lag en request context
#Kontroll = create_app()

#from BLOG import views