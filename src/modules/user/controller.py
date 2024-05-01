from flask import Blueprint, request
import modules.user.service as user_service
import modules.utils.auth_middleware as auth_middleware

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.post("/register")
def register():
    body = request.get_json()
    return user_service.register_user(body["email"], body["password"], body["type"])


@user_bp.post("/login")
def login():
    body = request.get_json()
    return user_service.login_user(body["email"], body["password"])


@user_bp.get("/me")
@auth_middleware.jwt_auth
def get_me(user):
    return user_service.get_me(user["id"])


@user_bp.get("/mentor")
@auth_middleware.jwt_auth
def get_mentor(user):
    if user["type"] == "mentor":
        return {"error": "Mentors do not have mentors"}, 400
    return user_service.get_mentor(user["id"])


@user_bp.get("/mentees")
@auth_middleware.jwt_auth
def get_mentees(user):
    if user["type"] == "mentee":
        return {"error": "Mentees do not have mentees"}, 400
    return user_service.get_mentees(user["id"])


@user_bp.post("/profile")
@auth_middleware.jwt_auth
def create_profile(user):
    body = request.get_json()
    return user_service.create_profile(user["id"], body)


@user_bp.post("/change_password")
@auth_middleware.jwt_auth
def change_password(user):
    body = request.get_json()
    return user_service.change_password(user["id"], body)
