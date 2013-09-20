# encoding=utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from flask.ext import admin


admin = admin.Admin(name=u'Meistaramánuður', url="/4dm1n")
db = SQLAlchemy()

def configure_extensions(app):

    if not app.debug and not app.testing:
        Sentry(app)

    db.init_app(app)
    admin.init_app(app)
    from web.models import *
    from web.admin import *
