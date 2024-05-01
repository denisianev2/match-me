from webexteamssdk import WebexTeamsAPI, ApiError
import os

# message = (
#         f'Hi! \n\nThank you both for committing to this mentoring engagement.🌱\n\n '
#         f'We used an algorithm to match you as best we could, based on your preferences. '
#         f'We hope you find ways to connect, enjoy this engagement and find meaningful value in it!\n\n'

#         f'Mentee, please take the first step and agree on a time to meet with your mentor. '
#         f'Start with getting to know each other and setting rules of engagement. '
#         f'We recommend you meet once a month for 45-60 minutes for the next 6 months.'
#         f'Here’s the [Mentorship Guide](https://cisco.sharepoint.com/:p:/s/TalentDevelopment/EaXwlnDmM3BBiilmNJMykGkBoLCJPDt6PInR3-Ko_r22IA?e=TW90F1)'
#         f' given earlier along with an additional '
#         f'[FAQ](https://cisco-my.sharepoint.com/:w:/p/prossini/EaKSJP3UwVpMjMe0SOllYu0BNVAu8RIibgOp0vXg1OARYg?e=VZN4qz)'
#         f' for your reference.📚\n\n'
#         f'Look out for more tips in the global spaces in the next few weeks!💡\n\n'
#         f'The Webex Bot will remove itself from this space. Reach out directly if you have questions.\n\n'
#         f'Paula Rossini\nGlobal Program Manager'
#     )

message = """
Hi! \n\nThank you both for committing to this mentoring engagement.🌱\n\n
We used an algorithm to match you as best we could, based on your preferences.
We hope you find ways to connect, enjoy this engagement and find meaningful value in it!\n\n

Mentee, please take the first step and agree on a time to meet with your mentor.
Start with getting to know each other and setting rules of engagement.
We recommend you meet once a month for 45-60 minutes for the next 6 months.
Here’s the [Mentorship Guide](https://cisco.sharepoint.com/:p:/s/TalentDevelopment/EaXwlnDmM3BBiilmNJMykGkBoLCJPDt6PInR3-Ko_r22IA?e=TW90F1)
given earlier along with an additional
[FAQ](https://cisco-my.sharepoint.com/:w:/p/prossini/EaKSJP3UwVpMjMe0SOllYu0BNVAu8RIibgOp0vXg1OARYg?e=VZN4qz)
for your reference.📚\n\n

Look out for more tips in the global spaces in the next few weeks!💡\n\n
The Webex Bot will remove itself from this space. Reach out directly if you have questions.\n\n
Paula Rossini\nGlobal Program Manager
"""

webex_client = WebexTeamsAPI(access_token=os.getenv(key="WEBEX_ACCESS_TOKEN"))


def create_webex_room(room_title: str, person_1_email: str, person_2_email: str) -> str:
    created_room = webex_client.rooms.create(room_title, teamId=None)

    webex_client.memberships.create(
        created_room.id, personId=None, personEmail=person_1_email, isModerator=True
    )
    webex_client.memberships.create(
        created_room.id, personId=None, personEmail=person_2_email, isModerator=True
    )

    webex_client.messages.create(
        created_room.id,
        parentId=None,
        toPersonId=None,
        toPersonEmail=None,
        text=None,
        markdown=message,
        files=None,
        attachments=None,
    )

    return created_room.id


def remove_room(room_id: str):
    webex_client.rooms.delete(room_id)
