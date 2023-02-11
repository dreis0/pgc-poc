from datetime import datetime

from flask import request, jsonify, Flask
import jwt


class AuthMiddleware:
    white_listed_routes = [
        "/auth/login",
        "/auth/register",
    ]

    secret = None
    app = None

    def __init__(self, app: Flask, secret):
        self.secret = secret
        self.app = app
        app.before_request(self.authenticate)

    def authenticate(self):
        if request.path not in self.white_listed_routes:
            token = request.headers.get("Authorization")
            if token is None:
                return jsonify({"error": "not authenticated no token"}), 401
            else:
                try:
                    payload = jwt.decode(token, self.secret, algorithms=["HS256"])

                    if payload["exp"] < datetime.now().timestamp():
                        return jsonify({"error": f"not authenticated expired"}), 401
                except Exception as e:
                    return jsonify({"error": f"not authenticated {e}"}), 401
