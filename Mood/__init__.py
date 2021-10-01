from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mde import Mde
from Mood.config import Config

# Declaring Extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mde = Mde()  # To be removed


def create_app(config_class=Config):
    app: Flask = Flask(__name__)
    app.config.from_object(Config)

    # initializing Extensions
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    mde.init_app(app)

    # import routes
    from Mood.blueprints import (
        main,
        auth,
        account,
        pubs,
        admin,
        room,
        errors
    )

    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(account)
    app.register_blueprint(pubs)
    app.register_blueprint(admin)
    app.register_blueprint(errors)
    app.register_blueprint(room)

    return app
