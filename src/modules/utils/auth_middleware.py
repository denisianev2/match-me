from functools import wraps
from flask import request, abort, jsonify
import jwt
import os


def jwt_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Authorization" not in request.headers and not request.headers[
            "Authorization"
        ].startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = request.headers["Authorization"].split(" ")[1]
        user = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return f(user, *args, **kwargs)

    return decorated_function
