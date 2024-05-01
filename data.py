"""
functions to read in the initial data files taken from the questionnaire
"""

__primary_author__ = "Vanessa Rottke"
__secondary_author__ = "Boaz Kwakkel"
__version__ = "1.1"

# Imports
import pandas as pd
from sklearn.metrics import jaccard_score
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pendulum


# Class to load data and select columns

class LoadData:

    def __init__(self, path_mentee, path_mentor):
        self.data_mentee = pd.read_excel(path_mentee, index_col=False)
        self.data_mentor = pd.read_excel(path_mentor, index_col=False)

    def select_column_mentee(self, column_name):
        column_mentee = self.data_mentee[column_name]
        return column_mentee
    
    def select_column_mentor(self, column_name):
        column_mentor = self.data_mentor[column_name]
        return column_mentor
    
    def compare_mentee(self, attribute_mentee, attribute_mentee_list):
        attribute_mentee_matrix = []
        for i in range(len(attribute_mentee)):
            row = []
            for j in range(len(attribute_mentee_list)):
                if attribute_mentee_list[j] in set(attribute_mentee[i].split(";")):
                    row.append(1)
                else:
                    row.append(0)
            attribute_mentee_matrix.append(row)
        return attribute_mentee_matrix

    def compare_mentor(self, attribute_mentor, attribute_mentor_list):
        attribute_mentor_matrix = []
        for i in range(len(attribute_mentor)):
            row = []
            for j in range(len(attribute_mentor_list)):
                if "I'm flexible and will adapt to my mentee's goals" in set(attribute_mentor[i].split(";")):
                    row = [1, 1, 1]
                elif attribute_mentor_list[j] in set(attribute_mentor[i].split(";")):
                    row.append(1)
                else:
                    row.append(0)
            attribute_mentor_matrix.append(row)
        return attribute_mentor_matrix
    
    def calculate_jaccard_matrix(self, mentor_attribute_matrix, mentee_attribute_matrix):
        jaccard_matrix = []
        for l in range(len(mentee_attribute_matrix)):
            row_j = []
            for m in range(len(mentor_attribute_matrix)):
                value = jaccard_score(mentee_attribute_matrix[l], mentor_attribute_matrix[m])
                row_j.append(value)
            jaccard_matrix.append(row_j)
        return jaccard_matrix

    def classify_mentor_role(self, data_role_mentor, data_technical_role_mentor):
        data_mentor_about_role = []
        for i in range(len(data_role_mentor)):
            if data_technical_role_mentor[i] == True:
                data_mentor_about_role.append('Technical role')
            else:
                data_mentor_about_role.append('Sales role')
        return data_mentor_about_role

    def filter_mentor_exec(self, jaccard_matrix, mentor_title_data):
        for j in range(len(jaccard_matrix[0])):
            if mentor_title_data[j] == True:
                for i in range(len(jaccard_matrix)):
                    jaccard_matrix[i][j] = jaccard_matrix[i][j]*1.5
        return jaccard_matrix

    def matching_data(self, mentee_about_info, mentor_about_info):
        match_matrix = []
        for i in range(len(mentee_about_info)):
            row = []
            for j in range(len(mentor_about_info)):
                if mentee_about_info[i] == mentor_about_info[j]:
                    row.append(1)
                else:
                    row.append(0)
            match_matrix.append(row)
        return match_matrix

    def filter_mentor_tech_role_data(self, jaccard_matrix, mentor_tech_role_pref, mentee_about_info):
        for j in range(len(jaccard_matrix[0])):
            if mentor_tech_role_pref[j] == "Technical role":
                for i in range(len(jaccard_matrix)):
                    if mentee_about_info[i] == "ASE":
                        jaccard_matrix[i][j] = jaccard_matrix[i][j]*1.5
        return jaccard_matrix
    
    def filter_mentor_sales_role_data(self, jaccard_matrix, mentor_sales_role_pref, mentee_about_info):
        for j in range(len(jaccard_matrix[0])):
            if mentor_sales_role_pref[j] == "Sales role":
                for i in range(len(jaccard_matrix)):
                    if mentee_about_info[i] == "ASR":
                        jaccard_matrix[i][j] = jaccard_matrix[i][j]*1.5
        return jaccard_matrix

    def filter_data_priority1(self, jaccard_matrix, mentee_pref_1, data_pref_1, match_matrix):
        for i in range(len(jaccard_matrix)):
            if mentee_pref_1[i] == data_pref_1: 
                for j in range(len(jaccard_matrix[i])):
                    if match_matrix[i][j] == 1:
                        jaccard_matrix[i][j] = jaccard_matrix[i][j]*2
        return jaccard_matrix

    def filter_data_priority2(self, jaccard_matrix, mentee_pref_2, data_pref_2, match_matrix):
        for i in range(len(jaccard_matrix)):
            if mentee_pref_2[i] == data_pref_2: 
                for j in range(len(jaccard_matrix[i])):
                    if match_matrix[i][j] == 1:
                        jaccard_matrix[i][j] = jaccard_matrix[i][j]*1.5
        return jaccard_matrix

    def filter_data_mentor(self, jaccard_matrix, mentor_pref, info_pref, match_matrix):
        for j in range(len(jaccard_matrix[0])):
            if mentor_pref[j] == info_pref: 
                for i in range(len(jaccard_matrix)):
                    if match_matrix[i][j] == 1:
                        jaccard_matrix[i][j] = jaccard_matrix[i][j]*1.5
        return jaccard_matrix
    
    def tz_diff(self, dic, country_1, country_2, on=None):

        if country_1 in dic and country_2 in dic:
            diff = (dic[country_1] - dic[country_2]).total_hours()

            if abs(diff) > 12.0:
                if diff < 0.0:
                    diff += 24.0
                else:
                    diff -= 24.0

            return abs(diff), dic

        """
        
        added timeout = None for now as Geolocator kept crashing
        please NOTE: if your code runs forever without results,
        there might be a Geolocator issue that is not timed out
        
        if an error with permissions occurs, change the user_agent.
        
        """
        geolocator = Nominatim(user_agent="mentor_mentree_algorithm")
        location_1 = geolocator.geocode(country_1, timeout = None)
        location_2 = geolocator.geocode(country_2, timeout = None)
        obj = TimezoneFinder()

        result_1 = obj.timezone_at(lng=location_1.longitude, lat=location_1.latitude)
        result_2 = obj.timezone_at(lng=location_2.longitude, lat=location_2.latitude)

        if on is None:
            on = pendulum.today()
        diff = (on.set(tz=result_1) - on.set(tz=result_2)).total_hours()
        dic[country_1]=on.set(tz=result_1)
        dic[country_2]=on.set(tz=result_2)

        if abs(diff) > 12.0:
            if diff < 0.0:
                diff += 24.0
            else:
                diff -= 24.0

        return abs(diff), dic

    def remove_row_column(self, matrix, i, j):
        for k in range(len(matrix[i])):
            matrix[i][k] = 0
        for l in range(len(matrix)):
            matrix[l][j] = 0
        return matrix

    def pair_row(self, matrix, i):
        max_val = [i,0,0] 
        for j in range(len(matrix[i])):
            if matrix[i][j] > max_val[2]:
                max_val = [i,j,matrix[i][j]] 
        return max_val[0], max_val[1], max_val[2]



