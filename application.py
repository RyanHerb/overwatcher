from flask import Flask, render_template, request, redirect, url_for 
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from sqlalchemy.orm import joinedload

from datetime import datetime

from models import *
from default import api

def create_app():
    app = Flask(__name__)

    app.register_blueprint(api)

    Bootstrap(app)

    db.init_app(app)
    return app

app = create_app()
app.config.from_object('config.DevelopmentConfig')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

def init_db():
    with app.app_context():
        db.create_all()


@app.teardown_appcontext
def shutdown_session(exception=None):
        db.session.remove()

if __name__ == '__main__':
    manager.run()
