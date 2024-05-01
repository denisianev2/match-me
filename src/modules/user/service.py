import os
import argon2
from modules.db import db
from flask import jsonify
import jwt

ARGON_SALT = os.getenv("ARGON_SALT")


def login_user(email: str, password: str):
    # TODO: validate body?
    user = db.get_user(email)
    if not user:
        return jsonify({"error": "User not found"}), 404
    # TODO: do we have to catch this exception? cant it return a boolean?
    try:
        if argon2.verify_password(
            bytes(user["password_hash"], "utf-8"), bytes(password, "utf-8")
        ):
            return (
                jsonify(
                    {
                        "token": jwt.encode(
                            {"id": user["id"], "type": user["type"]},
                            key=os.getenv("JWT_SECRET"),
                        )
                    }
                ),
                200,
            )
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid password"}), 401


def register_user(email: str, password: str, type: str):
    user = db.get_user(email)
    if user:
        return jsonify({"error": "User already exists"}), 400

    password_hash = argon2.hash_password(
        bytes(password, "utf-8"), bytes(ARGON_SALT, "utf-8")
    )

    db.insert_user(email, password_hash.decode(), type)
    return jsonify({"message": "User created"}), 201


def get_me(user_id: int):
    user = db.get_safe_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


def get_mentor(user_id):
    mentor = db.get_user_mentor(user_id=user_id)
    return jsonify(mentor), 200


def get_mentees(user_id):
    mentees = db.get_user_mentees(user_id=user_id)
    return jsonify(mentees), 200


def create_profile(user_id, body):
    # TODO validate body
    user = db.get_safe_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user["profile"]:
        return jsonify({"error": "Profile already exists"}), 400

    print(body)

    db.insert_profile(user_id=user_id, **body)
    return jsonify({"message": "Profile created"}), 201


def change_password(user_id, body):
    user = db.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        argon2.verify_password(
            bytes(user["password_hash"], "utf-8"), bytes(body["old_password"], "utf-8")
        )
    except Exception:
        return jsonify({"error": "Invalid password"}), 400

    password_hash = argon2.hash_password(
        bytes(body["new_password"], "utf-8"), bytes(ARGON_SALT, "utf-8")
    )

    db.change_password(user_id, password_hash.decode())
    return jsonify({"message": "Password updated"}), 200
