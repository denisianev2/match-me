"""
Delete rooms based on a chosen_room parameter and a specific api token.
"""

__author__ = "Boaz Kwakkel"
__version__ = "1.0"

# Imports
from webexteamssdk import WebexTeamsAPI

bot_api = WebexTeamsAPI(access_token='READ IN TOKEN FROM ENVIRONMENT HERE')


def delete_room(chosen):
    rooms = bot_api.rooms.list(me=True)
    for room in rooms:
        if room.title == chosen:
            print(f"Room ID: {room.id}")
            print(f"Room Title: {room.title}")
            print("------------------------")
            bot_api.rooms.delete(roomId=room.id)


chosen_room = "CSAP Mentoring – Club Cisco/Hall of Fame"

delete_room(chosen_room)
