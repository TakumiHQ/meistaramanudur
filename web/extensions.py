from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

db = SQLAlchemy()

def configure_extensions(app):

    if not app.debug and not app.testing:
        Sentry(app)

    db.init_app(app)
