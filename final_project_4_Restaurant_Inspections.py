"""
Final Project
DS-542

Arvind Rambahal

My Cuisine: Thai
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

my_cuisine = 'Thai'

data_url = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv?$limit=100000000000"
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

# Question 1
class Citation:
    def __init__(self, camis, dba, boro, street, zip_code, cuisine,
                 inspection_date, action, violation_code,
                 violation_description, critical_flag, latitude, longitude,
                 bin, bbl):
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
        self.latitude = handleNanString(latitude)
        self.longitude = handleNanString(longitude)
        self.bin = handleNanString(bin)
        self.bbl = handleNanString(bbl)
        
    def __repr__(self):
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
    
    def restaurant_closed(self):
        closed_string = "Establishment Closed by DOHMH"
        return(closed_string in self.action)

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
                                                                    food_data['critical_flag'][i],
                                                                    food_data['latitude'][i], 
                                                                    food_data['longitude'][i],
                                                                    food_data['bin'][i],
                                                                    food_data['bbl'][i]))
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
                                                                    food_data['critical_flag'][i],
                                                                    food_data['latitude'][i],
                                                                    food_data['longitude'][i],
                                                                    food_data['bin'][i],
                                                                    food_data['bbl'][i]))

# Question 2

# Analyze the violations for Thai Cuisine related to rodents and cockroaches
rat_violation_count = 0
mice_violation_count = 0
roach_violation_count = 0

camis_list = list(camis_dictionary.keys())

# Violations related to mice, rats, and roaches
for camis in camis_list:
    for citation in camis_dictionary[camis]:
        if citation.hasRats():
            rat_violation_count += 1
            
        if citation.hasMice():
            mice_violation_count += 1
            
        if citation.hasRoaches():
            roach_violation_count += 1

print(f"Rat Violations: {rat_violation_count}")
print(f"Mice Violations: {mice_violation_count}")
print(f"Roach Violations: {roach_violation_count}")

# Ratio - Rodent to roach citation
rodent_roach_ratio = (rat_violation_count + mice_violation_count) // roach_violation_count

# Question 3
# Analyze the frequent violators

# Counting the violations for each borough
borough_citation_dictionary = {"Manhattan": 0, "Bronx": 0, "Brooklyn": 0, "Queens": 0, "Staten Island": 0}

for camis in camis_list:
    for citation in camis_dictionary[camis]:
        borough_citation_dictionary[citation.boro] += 1

# Determine Borough with the most violations
max_value = max(borough_citation_dictionary.values())

for key, value in borough_citation_dictionary.items():
    if value == max_value:
        print(f"Borough with the most violations: {key}, {value} violations")

# The restaurant with the most violations
rest_most_vio = ["", 0]

for key, value in camis_dictionary.items():
    current_size = len(value)
    
    if(current_size > rest_most_vio[1]):
        rest_most_vio[0] = key
        rest_most_vio[1] = current_size

print("Restaurant with the most violations:")
print(f"{camis_dictionary[rest_most_vio[0]][0].dba}, {camis_dictionary[rest_most_vio[0]][0].street}, " + 
      f"{camis_dictionary[rest_most_vio[0]][0].boro}, {rest_most_vio[1]} violations")

# Check if restaurant closed. If so, how many times
most_violations_camis = rest_most_vio[0]
total_closure = 0

for citation in camis_dictionary[most_violations_camis]:
    if(citation.restaurant_closed()):
        total_closure += 1

print(f"Total times {camis_dictionary[rest_most_vio[0]][0].dba} closed: {total_closure}")


# Extra Credit

# Pie Chart, the share of 'rat' violations split by Borough

rat_violations_borough = {"Manhattan": 0, "Bronx": 0, "Brooklyn": 0, "Queens": 0, "Staten Island": 0}

for camis in camis_list:
    for citation in camis_dictionary[camis]:
        if(citation.hasRats()):
            rat_violations_borough[citation.boro] += 1
            
y = np.array(list(rat_violations_borough.values()))
borough_label = list(rat_violations_borough.keys())

# Formats pie, adds necessary padding to make it look nice
plt.style.use("fivethirtyeight")

# Creating the pie plot
plt.pie(y, autopct = "%1.1f%%", 
        shadow = True,
        wedgeprops= {"edgecolor" : "black",
                     "linewidth": 1,
                     "antialiased": True},
        explode = [0.1, 0, 0.1, 0, 0])

plt.title("Rat Violations By Borough for " + my_cuisine + " Restaurants")
plt.tight_layout()

plt.axis('equal')

plt.legend(borough_label, title = "Borough", loc = "lower right", fontsize = "xx-small")
plt.show()

# # Generate a map plot of violations for your cuisine over a map of NYC

# # Must install Geopandas:
# # Anaconda install: conda install geopandas
# # PIP install: pip install geopandas
# import geopandas as gpd

# # Download NYC shapefile from NYC OpenDataPortal:
# # https://data.cityofnewyork.us/Housing-Development/Shapefiles-and-base-map/2k7f-6s2k

# # Read NYC shapefile (must set path to shapefile)
# shapefile_path = r"C:\Users\arvin_g8r3xjo\OneDrive\Desktop\Saint Peter's University\Year4\Spring2024\DS_542\FinalProject_DS_542\Shapefiles and base map\geo_export_a20a6172-bb13-4ec6-a70b-238a07212f0d.shp"

# nyc_map = gpd.read_file(shapefile_path)

# # Plot map of NYC
# # fig, ax = plt.subplots(figsize=(10, 10))
# # nyc_map.plot(ax = ax, alpha = 0.5, color= 'black', edgecolor = 'black')

# long_lat_data = {'Longitude': [], 
#                   'Latitude': []}

# for camis in camis_list:
#     for citation in camis_dictionary[camis]:
#         long_lat_data['Longitude'].append(citation.longitude)
#         long_lat_data['Latitude'].append(citation.latitude)

# long_lat_df = pd.DataFrame.from_dict(long_lat_data)

# # using geopandas to convert long and lat to points
# df_geo = gpd.GeoDataFrame(long_lat_df, geometry = gpd.points_from_xy(
#     long_lat_df.Longitude, long_lat_df.Latitude))

# # plot points and map

# # Plot map of NYC
# fig, axis = plt.subplots(figsize=(10, 10))
# nyc_map.plot(ax = axis, color= 'lightblue', edgecolor = 'black')

# #axis = nyc_map.plot(color = 'lightblue', edgecolor = 'black')

# df_geo.plot(ax = axis, color = 'red')
# fig = matplotlib.pyplot.gcf()
# fig.set_size_inches(9, 6)

# plt.show()