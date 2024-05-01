from flask import Blueprint, jsonify
import modules.db.db as db


def remove_mentor_link(user_id: int, mentor_id: int):
    mentee_mentor_link = db.get_mentor_mentee_link(user_id, mentor_id)
    if not mentee_mentor_link:
        return {"error": "Unauthorised"}, 400
    db.delete_mentor_mentee_link(user_id, mentor_id)
    return {"message": "Mentee removed"}, 200
