"""
Execute the file to create an excel file with matched pairs of mentors and mentees based on the given parameters
"""

__primary_author__ = "Vanessa Rottke"
__secondary_author__ = "Boaz Kwakkel"
__version__ = "2.0"

import pandas as pd
import numpy as np
import xlsxwriter
import copy
import data

# Load the xlxs files into a data variable
# NOTE: PLEASE CHANGE FILEPATHS TO LOCAL FILEPATHS BEFORE USAGE

path_mentee = "fixed_mentee.xlsx"
path_mentor = "fixed_mentor.xlsx"
data = data.LoadData(path_mentee, path_mentor)

# Comparison for what mentor wants to give and mentee wants to get

get_mentee = data.select_column_mentee(
    "What are you most likely to want out of this mentoring engagement?"
)
give_mentor = data.select_column_mentor(
    "What are you most likely to give in this mentoring engagement?"
)

get_mentee_list = [
    "General strategic career advice",
    "Tactical day to day situations & problem solving",
    "Specific career advice to prepare for next role",
]
give_mentor_list = [
    "General strategic career advice depending on mentee goals",
    "Tactical day to day situations & problem solving",
    "Specific career advice to prepare for next role",
]

get_mentee_mat = data.compare_mentee(get_mentee, get_mentee_list)
give_mentor_mat = data.compare_mentor(give_mentor, give_mentor_list)


# Comparison for strengths of mentee and mentor

strength_mentee = data.select_column_mentee(
    "What are the strengths you'd like to further develop?"
)
strength_mentor = data.select_column_mentor("What are you general strengths?")

strength_list = [
    "Accountability",
    "Change management",
    "Coaching",
    "Collaboration",
    "Communications (public speaking)",
    "Competitive strategy",
    "Creativity / innovation",
    "Critical thinking",
    "Cross-architecture",
    "Crucial conversations",
    "Customer interaction",
    "Decision making",
    "Delegating",
    "Design thinking",
    "Effective listening",
    "Empowerment",
    "Finance",
    "Goal setting",
    "Influencing",
    "Negotiating",
    "Personal Brand",
    "Prioritization",
    "Productivity",
    "Providing feedback",
    "Recognition",
    "Social Media",
    "Story telling",
    "Team building",
    "Technical knowledge",
    "Time management",
    "Transition career path",
    "Work / Life balance",
]

strength_mentee_mat = data.compare_mentee(strength_mentee, strength_list)
strength_mentor_mat = data.compare_mentor(strength_mentor, strength_list)


# Comparison for interests of mentee and mentor
# currently have by hand added none and non1

interest_mentee = data.select_column_mentee("What are your personal interests?")
interest_mentor = data.select_column_mentor("What are your personal interests?")

interest_list = [
    "Art",
    "Cooking",
    "Culture",
    "Dance",
    "Design",
    "Extreme sports (sky diving)",
    "Family",
    "Gardening",
    "Individual sports (golf, running)",
    "Meditation",
    "Music",
    "Pets",
    "Photography",
    "Politics",
    "Puzzles & games",
    "Reading",
    "Religion",
    "Shopping/fashion",
    "Social networking",
    "Team sports (soccer, football)",
    "Tech hobbies",
    "Travel",
    "Volunteering",
    "Wine tasting",
    "Working out",
    "None",
    "None1",
]

interest_mentee_mat = data.compare_mentee(interest_mentee, interest_list)
interest_mentor_mat = data.compare_mentor(interest_mentor, interest_list)


# Create one matrix for mentee and mentos with all attributes

mentee_mat_pos1 = np.array(get_mentee_mat)
mentee_mat_pos2 = np.array(strength_mentee_mat)
mentee_mat_pos3 = np.array(interest_mentee_mat)
mentee_mat = np.concatenate((mentee_mat_pos1, mentee_mat_pos2, mentee_mat_pos3), axis=1)

mentor_mat_pos1 = np.array(give_mentor_mat)
mentor_mat_pos2 = np.array(strength_mentor_mat)
mentor_mat_pos3 = np.array(interest_mentor_mat)
mentor_mat = np.concatenate((mentor_mat_pos1, mentor_mat_pos2, mentor_mat_pos3), axis=1)


# Calculate Jaccard similarity matrix

jaccard_mat = data.calculate_jaccard_matrix(mentor_mat, mentee_mat)

# Classify mentor roles into technical or sales
role_mentor = data.select_column_mentor("What is your title?")
technical_list = "Architect|Engineer|Technical|Systems|TSA|Specialist|SE|ASE|Tech"
sales_list = "Sales|Account|Business|Strategic|Partner|Territory|Customer|AM|ASR|Sales"
technical_role_mentor = np.array(role_mentor.str.contains(technical_list))
sales_role_mentor = np.array(role_mentor.str.contains(sales_list))
mentor_about_role = data.classify_mentor_role(role_mentor, technical_role_mentor)

# Load mentor/mentee preferences
mentee_pref1 = data.select_column_mentee(
    "If possible, what's your first priority in matching you with a mentor?"
)
mentee_pref2 = data.select_column_mentee(
    "If possible, what's your second priority in matching you with a mentor?"
)

# Create mentor matrix with necessary information
mentor_about_gender = data.select_column_mentor("How would you describe your gender?")
mentor_about_theatre = data.select_column_mentor("Your theatre?")
mentor_about_segment = data.select_column_mentor("Your segment?")
mentor_about = pd.concat(
    (mentor_about_gender, mentor_about_theatre, mentor_about_segment), axis=1
)

# Create mentor matrix with necessary information
mentee_about_gender = data.select_column_mentee("How would you describe your gender?")
mentee_about_theatre = data.select_column_mentee("Your theatre?")
mentee_about_segment = data.select_column_mentee(
    "If possible, which segment would you like your mentor to be from?"
)
mentee_about = pd.concat(
    (mentee_about_gender, mentee_about_theatre, mentee_about_segment), axis=1
)


# Calculate 1st priority weight
match_matrix_gender = data.matching_data(mentee_about_gender, mentor_about_gender)
jaccard_mat = data.filter_data_priority1(
    jaccard_mat, mentee_pref1, "Gender", match_matrix_gender
)

match_matrix_theatre = data.matching_data(mentee_about_theatre, mentor_about_theatre)
jaccard_mat = data.filter_data_priority1(
    jaccard_mat, mentee_pref1, "Theatre", match_matrix_theatre
)

match_matrix_segment = data.matching_data(mentee_about_segment, mentor_about_segment)
jaccard_mat = data.filter_data_priority1(
    jaccard_mat, mentee_pref1, "Segment", match_matrix_segment
)

mentee_about_role = data.select_column_mentee(
    "If possible, would you prefer a mentor in a:"
)
match_matrix_segment = data.matching_data(mentee_about_role, mentor_about_role)
jaccard_mat = data.filter_data_priority1(
    jaccard_mat, mentee_pref1, "Role (Tech/Sales)", match_matrix_segment
)

# Calculate 2nd priority weight
jaccard_mat = data.filter_data_priority2(
    jaccard_mat, mentee_pref2, "Gender", match_matrix_gender
)

jaccard_mat = data.filter_data_priority2(
    jaccard_mat, mentee_pref2, "Theatre", match_matrix_theatre
)

jaccard_mat = data.filter_data_priority2(
    jaccard_mat, mentee_pref2, "Segment", match_matrix_segment
)

jaccard_mat = data.filter_data_priority2(
    jaccard_mat, mentee_pref2, "Role (Tech/Sales)", match_matrix_segment
)


# Calculate weights for mentor priorities
mentor_pref_theatre = data.select_column_mentor(
    "Would you prefer a mentee in the same theatre?"
)
mentor_pref_gender = data.select_column_mentor(
    "Would you prefer a mentee of the same gender?"
)
mentor_pref_role = data.select_column_mentor("Would you prefer a mentee in a:")

jaccard_mat = data.filter_data_mentor(
    jaccard_mat, mentor_pref_theatre, "Yes", match_matrix_theatre
)
jaccard_mat = data.filter_data_mentor(
    jaccard_mat, mentor_pref_theatre, "Yes", match_matrix_theatre
)

mentee_about_csap_track = data.select_column_mentee("Your CSAP track")

jaccard_mat = data.filter_mentor_tech_role_data(
    jaccard_mat, mentor_pref_role, mentee_about_csap_track
)
jaccard_mat = data.filter_mentor_sales_role_data(
    jaccard_mat, mentor_pref_role, mentee_about_csap_track
)


# Give higher priority to executive roles
executive_list = "Director|Lead"
exec_role_mentor = np.array(role_mentor.str.contains(executive_list))
jaccard_mat = data.filter_mentor_exec(jaccard_mat, exec_role_mentor)

# Prioritize mentors with VP/executive title
jaccard_mat = data.filter_mentor_exec(jaccard_mat, exec_role_mentor)

# Filter data for large time zone differences
country_mentor = data.select_column_mentor("Your country of residence")
country_mentee = data.select_column_mentee("Your country of residence")

# Variable for the max difference in time zones
max_difference_timezone = 6

country_dic = {}
tz_diff_matrix = []
for i in range(len(country_mentee)):
    row = []
    for j in range(len(country_mentor)):
        time, country_dic = data.tz_diff(
            country_dic, country_mentee[i], country_mentor[j]
        )
        print(time)
        row.append(time)
    tz_diff_matrix.append(row)

for i in range(len(jaccard_mat)):
    for j in range(len(jaccard_mat[i])):

        # If the max timezone is exceeded, remove the match from the matrix
        if tz_diff_matrix[i][j] > max_difference_timezone:
            jaccard_mat[i][j] = jaccard_mat[i][j] * 0


# Find/Ensure unique pairs for each mentor/mentee
max_val_mat = [[], [], []]

# Set the amount of matches that you want in the generated eXcel sheet:
amount_of_matches = 3

# Create the amount of unique matches needed
for round in range(amount_of_matches):
    copy_jaccard_mat = copy.deepcopy(jaccard_mat)
    for i in range(len(copy_jaccard_mat)):
        i, j, score = data.pair_row(copy_jaccard_mat, i)
        max_val_mat[round].append([i, j, score])
        data.remove_row_column(copy_jaccard_mat, i, j)
    for element in max_val_mat[round]:
        jaccard_mat[element[0]][element[1]] = 0
print(max_val_mat)


# Map to mentor/mentee ID, Name, Email

mentor_id = data.select_column_mentor("ID")
mentor_name = data.select_column_mentor("Name")
mentor_email = data.select_column_mentor("Email")

mentee_id = data.select_column_mentee("ID")
mentee_name = data.select_column_mentee("Name")
mentee_email = data.select_column_mentee("Email")

for round in range(amount_of_matches):
    for i in range(len(max_val_mat[round])):
        max_val_mat[round][i].insert(3, mentee_id[i])
        max_val_mat[round][i].insert(4, mentee_name[i])
        max_val_mat[round][i].insert(5, mentee_email[i])
        max_val_mat[round][i].insert(6, mentor_id[max_val_mat[round][i][1]])
        max_val_mat[round][i].insert(7, mentor_name[max_val_mat[round][i][1]])
        max_val_mat[round][i].insert(8, mentor_email[max_val_mat[round][i][1]])
    [j.pop(0) for j in max_val_mat[round]]
    [j.pop(0) for j in max_val_mat[round]]
    [j.pop(0) for j in max_val_mat[round]]


# Export to Excel

# Set name for the final document
export_xlsx = "matches_24_standard.xlsx"

workbook = xlsxwriter.Workbook(export_xlsx)
for round in range(amount_of_matches):
    worksheet = workbook.add_worksheet(f"Rank_{round+1}")
    worksheet.write("A1", "Mentee ID")
    worksheet.write("B1", "Mentee Name")
    worksheet.write("C1", "Mentee Email")
    worksheet.write("D1", "Mentor ID")
    worksheet.write("E1", "Mentor Name")
    worksheet.write("F1", "Mentor Email")
    for row_num, data in enumerate(max_val_mat[round]):
        worksheet.write_row(row_num + 1, 0, data)

workbook.close()
