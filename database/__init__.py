from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

#
# def configure_database(app: Flask, db: SQLAlchemy):
#     app.logger.info("Configuring database")
#
#     with app.app_context():
#         Base.metadata.create_all(db.engine)
#
#     app.logger.info("Database configured")
