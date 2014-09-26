# encoding=utf-8

import os
import datetime

from flask import Flask, current_app, url_for


def create_app():

    app = Flask(__name__, static_folder="../public")
    app.config.setdefault('STATIC_URL', os.environ.get('STATIC_URL'))
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', os.environ.get('DATABASE_URL'))
    app.config.setdefault('SECRET_KEY', os.environ.get('SECRET_KEY'))

    from web.extensions import configure_extensions
    configure_extensions(app)

    @app.context_processor
    def context():
        return dict(
            today=datetime.date.today(),
            static=static,
        )

    from web.views import views
    app.register_blueprint(views)
    return app


def static(filename):
    if current_app.debug or current_app.config['STATIC_URL'] is None:
        return url_for('static', filename=filename)
    return current_app.config['STATIC_URL'] + filename


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        from web.extensions import db
        db.create_all()
    app.run(host='0.0.0.0', port=5010, debug=True)
