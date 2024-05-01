from flask import Blueprint, jsonify, request
import modules.utils.auth_middleware as auth_middleware
import modules.db.db as db
import modules.mentor.service as mentor_service

mentor_bp = Blueprint("mentor", __name__, url_prefix="/mentor")


@mentor_bp.get("/list")
@auth_middleware.jwt_auth
def get_all_mentors(user):
    return jsonify(db.get_all_safe_mentors()), 200


@mentor_bp.post("/unlink")
@auth_middleware.jwt_auth
def remove_mentee_link(user):
    return jsonify(
        mentor_service.remove_mentee_link(user["id"], request.json["mentee_id"])
    )
