"""
The purpose of this file is to automate the creation of webex teams spaces from a list of mentors/mentees stored in
an excel file. Included is an optional function to send an adaptive json card.
Additionally, the code removes the bot from the rooms after a short sleep time.
"""

__primary_author__ = "Vanessa Rottke"
__secondary_author__ = "Boaz Kwakkel"
__version__ = "2.0"


# Imports
from webexteamssdk import WebexTeamsAPI, ApiError
import time
import pandas as pd
from rich.console import Console
from rich.panel import Panel

console = Console()

"""
the token that is used determines who 'creates the group' and from whom the welcome message is sent out
You can use other people's tokens to create the rooms in their names if needed.
The current setup uses a bot token.
"""

bot_api = WebexTeamsAPI(access_token="READ IN TOKEN FROM ENVIRONMENT HERE")

# Read in your xlsx files.
path = 'test.xlsx'
xlsx = 'matched.xlsx'
df = pd.read_excel(path)

# Read the emails from the dataframe into variables
# Make sure to check if column names match column call
mentee_email = df.Mentee_Email
mentor_email = df.Mentor_Email
mentee_names = df.Mentee_Name
mentor_names = df.Mentor_Name

console.print(Panel.fit("Webex Space creation started"))
# Loop through the mentee emails, match them with the mentor emails and create rooms with the parameter set above
for i in range(len(mentee_email)):
    # Set the room title and create the room for people to be added
    room_title = 'CSAP Mentoring – Club Cisco/Hall of Fame'
    create_room = bot_api.rooms.create(room_title, teamId=None)
    room_id = getattr(create_room, 'id')

    # Read in the correct mentor and mentee

    mentee_email_i = mentee_email[i]
    mentor_email_i = mentor_email[i]

    # Allows us to specify the mentor and mentee by name. Currently only used for checking if run is correct
    mentee_name = mentee_names[i]
    mentor_name = mentor_names[i]

    # Check combination
    print(mentee_name + " ----- AND ---- " + mentor_name)

    # Create membership to the rooms
    bot_api.memberships.create(room_id, personId=None, personEmail=f'{mentee_email_i}', isModerator=True)
    bot_api.memberships.create(room_id, personId=None, personEmail=f'{mentor_email_i}', isModerator=True)

    # This message was composed by Paula Rossini. Please check whether still valid for new use case.
    message = (
        f'Hi! \n\nThank you both for committing to this mentoring engagement.🌱\n\n '
        f'We used an algorithm to match you as best we could, based on your preferences. '
        f'We hope you find ways to connect, enjoy this engagement and find meaningful value in it!\n\n'
        
        f'Mentee, please take the first step and agree on a time to meet with your mentor. '
        f'Start with getting to know each other and setting rules of engagement. '
        f'We recommend you meet once a month for 45-60 minutes for the next 6 months.'
        f'Here’s the [Mentorship Guide](https://cisco.sharepoint.com/:p:/s/TalentDevelopment/EaXwlnDmM3BBiilmNJMykGkBoLCJPDt6PInR3-Ko_r22IA?e=TW90F1)'
        f' given earlier along with an additional '
        f'[FAQ](https://cisco-my.sharepoint.com/:w:/p/prossini/EaKSJP3UwVpMjMe0SOllYu0BNVAu8RIibgOp0vXg1OARYg?e=VZN4qz)'
        f' for your reference.📚\n\n'
        f'Look out for more tips in the global spaces in the next few weeks!💡\n\n'
        f'The Webex Bot will remove itself from this space. Reach out directly if you have questions.\n\n'
        f'Paula Rossini\nGlobal Program Manager'
    )

    # Sent the set message into the room
    bot_api.messages.create(room_id, parentId=None, toPersonId=None, toPersonEmail=None, text=None, markdown=message,
                            files=None, attachments=None)

console.print(Panel.fit("Webex Space creation complete"))

# Check all created rooms for the correct pairing via the output log
rooms = bot_api.rooms.list(me=True)
for room in rooms:
    if room.title == 'CSAP Mentoring – Club Cisco/Hall of Fame':
        memberships = bot_api.memberships.list(roomId=room.id)
        for member in memberships:
            person = bot_api.people.get(member.personId)
            if person.displayName != "CSAP Mentorship FY24":
                print(person.displayName)
        print("----New Room----")

# Let all rooms be created properly
time.sleep(120)

console.print(Panel.fit("Starting bot removal"))
# Get the id of the bot
bot = bot_api.people.me()

# Get a list of rooms where the bot is a member
memberships = bot_api.memberships.list(personId=bot.id)

# Remove the bot from each room
for membership in memberships:
    try:
        bot_api.memberships.delete(membership.id)
        print(f'Bot removed from room: {membership.roomId}')

    # Give an exception option, as some rooms will be 1-0-1 rooms with the bot, which will crash the code if no
    # proper exception handling is implemented.
    except ApiError as e:
        print(f"Error removing bot from room {e}")

console.print(Panel.fit("File complete"))
