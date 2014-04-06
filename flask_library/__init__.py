# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask.ext.babel import Babel


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

csrf = CsrfProtect(app)

babel = Babel(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = u'Пожалуйста, войдите, чтобы получить доступ к этой странице.'
login_manager.login_message_category = 'info'

from flask_library import views, models, forms
