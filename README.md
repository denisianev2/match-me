# matching_algorithm
### author of original files: Vanessa Rottke 
### author of updated files and current documentation: Boaz Kwakkel
This purpose of the project was to create an algorithm that would uniquely match mentors and mentees with one another. The mentees and mentors were matched with one another based on various critieria, such as their preferences, interests, region/time zone, field of work, etc.

After the mentees and mentors had been matched with one another, a Webex space was automatically created for each pair.

The requirements.txt file contains all the necessary libraries for this project.

The files logged here and their purpose are as follows:
## Matching algorithm related:

data: stores the functions to read in the initial data files taken from the questionnaire.

mentor_matching_algorithm: primary code file for matching the mentors and mentees.

removing_chosen: outputs the mentors that were not picked by the algorithm so they can be notified.

## Webex space automation related:
delete_rooms: code to delete all rooms in which the Webex bot exists, purely for cleaning up any excess rooms.

webex_space_automation: code to automatically create webex spaces from an excel sheet listing pairs of mentors and mentees.

## Things to be careful with:
- As the files contain proprietary information, none of the xlsx files are attached with the handover. Please contact Paula Rossini for access to the files used this year.
- In similar fashion, the current bot-api token was removed entirely. Please create a new bot, or contact Boaz Kwakkel for the original CSAP Mentorship bot.
- current data reading is very specific to the questionnaire as set for the mentor/mentee program.
- empty rows can heavily impact the reading/final scores (this should be known to Paula and the option for a non-answer would ideally be removed).
- in the data file the function for geolocation might run into errors. See that specific function for advice on fixes.