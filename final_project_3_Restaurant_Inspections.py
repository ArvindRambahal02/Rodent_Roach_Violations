#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Project Template
DS 542

My Name: Arvind Rambahal
My Cuisine: Thai
"""

import pandas as pd

my_cuisine = 'Thai'

data_url = 'https://data.cityofnewyork.us/resource/43nn-pn8j.csv?$limit=10000000000'

food_data = pd.read_csv(data_url)

def handleNanString(item):
    if(pd.isna(item)):
        return ""
    else:
        return item
    
def convertCriticalFlagToBool(item):
    if(item == "Critical"):
        return True
    else:
        return False
    

"""
Answer all questions asked in the prompt.
Put your code to answer each question inside the comments that represent that question.
Print to the screen when you are asked for an answer.
"""

# Question 1

class Citation:
    
    def __init__(self, camis, dba, boro, street, zip_code, cuisine,
                 inspection_date, action, violation_code,
                 violation_description, critical_flag):
        self.camis = handleNanString(camis)
        self.dba = handleNanString(dba)
        self.boro = handleNanString(boro)
        self.street = handleNanString(street)
        self.zip_code = handleNanString(zip_code)
        self.cuisine = handleNanString(cuisine)
        self.inspection_date = handleNanString(inspection_date)
        self.action = handleNanString(action)
        self.violation_code = handleNanString(violation_code)
        self.violation_description = handleNanString(violation_description)
        self.critical_flag = handleNanString(convertCriticalFlagToBool(critical_flag))
    
    def __repr__(self):
        # return(f"Citation: {self.camis}, DBA: {self.dba}, Boro: {self.boro}, Street: {self.street}, " +
        #        f"Zip Code: {self.zip_code}, Cuisine_description: {self.cuisine}, Inspection Date: {self.inspection_date}, " +
        #        f"Action: {self.action}, Violation Code: {self.violation_code}, Violation Description: {self.violation_description}, " + 
        #        f"Critical Flag: {self.critical_flag}")
        
        return(f"Citation: {self.camis}, DBA: {self.dba}, Borough: {self.boro}, " + 
               f"Cuisine_description: {self.cuisine}, Violation Description: {self.violation_description}")
    
    def hasMice(self):
        mice_string = "Evidence of mice or live mice"
        return(mice_string in self.violation_description)
    
    def hasRats(self):
        rats_string = "Evidence of rats or live rats"
        return(rats_string in self.violation_description)
    
    def hasRoaches(self):
        roaches_string = "Live roaches"
        return(roaches_string in self.violation_description)
    
camis_dictionary = dict()
for i in range(len(food_data)):
    if food_data['cuisine_description'][i] == my_cuisine:
        if food_data['camis'][i] in camis_dictionary.keys():
            camis_dictionary[food_data['camis'][i]].append(Citation(food_data['camis'][i], 
                                                                    food_data['dba'][i], 
                                                                    food_data['boro'][i],
                                                                    food_data['street'][i],
                                                                    food_data['zipcode'][i],
                                                                    food_data['cuisine_description'][i],
                                                                    food_data['inspection_date'][i],
                                                                    food_data['action'][i], 
                                                                    food_data['violation_code'][i], 
                                                                    food_data['violation_description'][i], 
                                                                    food_data['critical_flag'][i]))
        else:
            camis_dictionary[food_data['camis'][i]] = []
            camis_dictionary[food_data['camis'][i]].append(Citation(food_data['camis'][i], 
                                                                    food_data['dba'][i], 
                                                                    food_data['boro'][i],
                                                                    food_data['street'][i],
                                                                    food_data['zipcode'][i],
                                                                    food_data['cuisine_description'][i],
                                                                    food_data['inspection_date'][i],
                                                                    food_data['action'][i], 
                                                                    food_data['violation_code'][i], 
                                                                    food_data['violation_description'][i], 
                                                                    food_data['critical_flag'][i]))

# Question 2

# Analyze the violations for Thai Cuisine related to rodents and cockroaches
rat_violation_count = 0
mice_violation_count = 0
roach_violation_count = 0

keys_list = list(camis_dictionary.keys())

# violations related to mice or rats
for key in keys_list:
    for citation in camis_dictionary[key]:
        if citation.hasRats():
            rat_violation_count += 1
            #print(citation)
        if citation.hasMice():
            mice_violation_count += 1
            #print(citation)
        if citation.hasRoaches():
            roach_violation_count += 1
            #print(citation)

# Ratio - Rodent to roach citation
rodent_roach_ratio = (rat_violation_count + mice_violation_count) // roach_violation_count

# Question 3

# Extra Credit