from flask import Blueprint, jsonify, request
import modules.utils.auth_middleware as auth_middleware
import modules.db.db as db
import modules.mentee.service as mentee_service

mentee_bp = Blueprint("mentee", __name__, url_prefix="/mentee")


@mentee_bp.get("/list")
@auth_middleware.jwt_auth
def get_all_mentors(user):
    return jsonify(db.get_all_safe_mentees()), 200


@mentee_bp.post("/unlink")
@auth_middleware.jwt_auth
def remove_mentor_link(user):
    return jsonify(
        mentee_service.remove_mentor_link(user["id"], request.json["mentor_id"])
    )
