"""
Outputs the mentors that were not picked by the algorithm so they can be notified.
"""

__author__ = "Boaz Kwakkel"
__version__ = "1.0"

import pandas as pd

# Read in both excel files
path_original = 'fixed_mentor.xlsx'
path_chosen = 'final_pairing.xlsx'
df = pd.read_excel(io=path_original)
df_chosen = pd.read_excel(io=path_chosen)


# Read names of chosen mentors into a list
all_mentor_names = df_chosen['chosen_mentors']
check = all_mentor_names.tolist()

# Check if all were successfully read into the list
print(check)
print(len(check))

# Use list to check for chosen mentors and save in 'Chosen' Column in dataframe
df['Chosen'] = (df['Name'].isin(check))
print(df)

# Drops any row where there is no 'False' detected
df = df.drop(df[df['Chosen'] == True].index)
print(df)

# Export to Excel file of choice
df.to_excel("NotChosen_Mentors.xlsx")
