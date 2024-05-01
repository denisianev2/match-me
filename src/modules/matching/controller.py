from flask import Blueprint, request
import modules.matching.service as matching_service
import modules.utils.auth_middleware as auth_middleware

matching_bp = Blueprint("match", __name__, url_prefix="/match")


@matching_bp.get("/")
@auth_middleware.jwt_auth
def get_match(user):
    return matching_service.match(user["id"])


@matching_bp.post("/")
@auth_middleware.jwt_auth
def add_mentor(user):
    return matching_service.add_mentee_mentor(user["id"], request.json["mentor_id"])


@matching_bp.post("/room")
@auth_middleware.jwt_auth
def create_room(user):
    if user["type"] == "mentee":
        return matching_service.create_webex_room(user["id"], request.json["mentor_id"])
    return matching_service.create_webex_room(request.json["mentee_id"], user["id"])


@matching_bp.delete("/room")
@auth_middleware.jwt_auth
def remove_room(user):
    if user["type"] == "mentee":
        return matching_service.remove_room(user["id"], request.json["mentor_id"])
    return matching_service.remove_room(request.json["mentee_id"], user["id"])
