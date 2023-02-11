from datetime import datetime, timedelta

import bcrypt as bcrypt
import jwt
from flask import Flask, Blueprint, jsonify, request, Response
from flask_sqlalchemy.session import Session
from sqlalchemy import select, insert

from database.auth_key import AuthKey


class AuthEndpoint:
    blueprint = None
    app = None
    db = None
    secret = None

    def __init__(self, app: Flask, db, secret: str):
        self.app = app
        self.db = db
        self.secret = secret
        self.blueprint = Blueprint('auth', __name__, url_prefix='/auth')

        self.blueprint.route('/register', methods=['POST'])(self.create_account)
        self.blueprint.route('/login', methods=['POST'])(self.login)

    def create_account(self):
        data = request.get_json()
        session = Session(self.db)

        query = select(AuthKey).where(AuthKey.name == data["name"])
        key = session.execute(query).first()

        if key is None:
            hashedKey = bcrypt.hashpw(data["key"].encode('utf-8'), bcrypt.gensalt())
            registration = AuthKey(name=data["name"], key=hashedKey.decode("utf-8"), description=data["description"])

            session.execute(insert(AuthKey), [registration.to_dict()])
            session.commit()

            token = self.generate_token(data["name"])

            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Account already exists"}), 400

    def login(self):
        data = request.get_json()
        session = Session(self.db)

        query = select(AuthKey).where(AuthKey.name == data["name"])
        user = session.execute(query).scalars().first()

        if user is None:
            return jsonify({"error": "Account does not exist"}), 400
        else:
            if bcrypt.checkpw(data["key"].encode('utf-8'), user.key.encode('utf-8')):
                token = self.generate_token(data["name"])

                return jsonify({"token": token}), 200
            else:
                return jsonify({"error": "Invalid login data"}), 400

    def generate_token(self, name):
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=12),
            'iat': datetime.utcnow(),
            'sub': name
        }

        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )
