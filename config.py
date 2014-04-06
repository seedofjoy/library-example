# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.dirname(__file__)


DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sqlite.db')

SECRET_KEY = 'seeecret'
WTF_CSRF_SECRET_KEY = 'very-secret-key-very-very'
WTF_I18N_ENABLED = True

BABEL_DEFAULT_LOCALE = 'ru'
