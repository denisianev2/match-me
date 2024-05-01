import modules.db.db as db
import modules.matching.jaccard as jaccard
import modules.utils.webex
import json


def match(user_id: int):
    user = db.get_safe_user(user_id)
    if not user:
        return {"error": "User not found"}, 404
    print(json.dumps(user, indent=2))
    instructors = db.get_all_safe_mentors()

    return {"matches": jaccard.match(user, instructors)}, 200


def add_mentee_mentor(user_id, mentor_id):
    user = db.get_safe_user(user_id)
    mentor = db.get_safe_user(mentor_id)
    if not user:
        return {"error": "User not found"}, 404
    if not mentor:
        return {"error": "Mentor not found"}, 404
    db.add_mentee_mentor(user_id, mentor_id)
    return {"message": "Added mentor"}, 200


def create_webex_room(mentee_id, mentor_id):
    mentee_mentor_link = db.get_mentor_mentee_link(mentee_id, mentor_id)
    if not mentee_mentor_link:
        return {"error": "Unauthorised"}, 400
    if mentee_mentor_link["room_id"] is not None:
        return {"error": "Room already exists"}, 400
    mentee = db.get_safe_user(mentee_id)
    mentor = db.get_safe_user(mentor_id)
    room_title = f"{mentee['user']['email']} and {mentor['user']['email']} Mentorship"
    room_id = modules.utils.webex.create_webex_room(
        room_title, mentee["user"]["email"], mentor["user"]["email"]
    )
    db.add_room(room_id, mentee_id, mentor_id)
    return {"room_id": room_id}, 200


def remove_room(mentee_id, mentor_id):
    mentee_mentor_link = db.get_mentor_mentee_link(mentee_id, mentor_id)
    if not mentee_mentor_link:
        return {"error": "Unauthorised"}, 400
    modules.utils.webex.remove_room(mentee_mentor_link["room_id"])
    db.delete_room(mentee_id, mentor_id)
    return {"message": "Room removed"}, 200
