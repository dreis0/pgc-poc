from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database.auth_key import AuthKey


def configure_database(app: Flask, db: SQLAlchemy):
    app.logger.info("Configuring database")

    with app.app_context():
        AuthKey().metadata.create_all(db.engine)

    app.logger.info("Database configured")
