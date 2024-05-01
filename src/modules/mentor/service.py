from flask import Blueprint, jsonify
import modules.db.db as db


def remove_mentee_link(user_id: int, mentee_id: int):
    mentee_mentor_link = db.get_mentor_mentee_link(mentee_id, user_id)
    if not mentee_mentor_link:
        return {"error": "Unauthorised"}, 400
    db.delete_mentor_mentee_link(mentee_id, user_id)
    return {"message": "Mentee removed"}, 200
