## Distance to city facilities
## Retrive Census data from Justice Map API

import os
import requests
import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
from scipy.spatial import distance

path = "F:/RetrofitPolicy/LA/" 
os.chdir(path)

################################## Functions ########################################
def haversine(lat1, lat2, lon1, lon2):
    
    R = 6372800
    
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return c*R/1000


def closest_node(node, nodes):
    
    closest_index = distance.cdist([node], nodes).argmin()
    return nodes[closest_index]
    
###################################### CBD #######################################
df = pd.read_csv('SoftStory_single.csv')

center_lat = 34.051001
center_lon = -118.257040

CBD = []

for index, row in df.iterrows():     
    lon = row['CENTER_LON']
    lat = row['CENTER_LAT']
    dist = haversine(lat, center_lat, lon, center_lon)
    CBD.append(dist)


################################## Facilities #####################################
park = pd.read_csv('Recreation_and_Parks_Facilities.csv')
school = pd.read_csv('School_District_Headquarter_locations.csv')
police = pd.read_csv('LAPD_Police_Stations.csv')
fire = pd.read_csv('Fire_Stations.csv')

park_nodes = park[['Y','X']].to_numpy()
school_nodes = school[['Y','X']].to_numpy()
fire_nodes = fire[['Y','X']].to_numpy()
police_nodes = police[['Y','X']].to_numpy()  

def distance_facilities(lon, lat):
    park = []; school = []; fire = []; police = []
       
    for i in range(0,len(lon)):
        park_index = closest_node((lat[i],lon[i]),park_nodes)
        park_dist = haversine(lat[i], park_index[0], lon[i], park_index[1])
        park.append(park_dist)  
           
        school_index = closest_node((lat[i],lon[i]),school_nodes)
        school_dist = haversine(lat[i], school_index[0], lon[i], school_index[1])
        school.append(school_dist)    
            
        fire_index = closest_node((lat[i],lon[i]),fire_nodes)
        fire_dist = haversine(lat[i], fire_index[0], lon[i], fire_index[1])
        fire.append(fire_dist)  
            
        police_index = closest_node((lat[i],lon[i]),police_nodes)
        police_dist = haversine(lat[i], police_index[0], lon[i], police_index[1])
        police.append(police_dist)
               
    d = {'Park':park,'School':school,'Police':police,'Fire':fire}
    return pd.DataFrame(data=d)


LON = df['CENTER_LON'].to_numpy()
LAT = df['CENTER_LAT'].to_numpy()
soft = distance_facilities(LON, LAT)
soft['CBD'] = CBD
soft['longitude'] = df['CENTER_LON']
soft['latitude'] = df['CENTER_LAT']
soft = pd.concat([soft,df], axis=1)
soft.dropna(how='any', inplace=True)  # Drop the rows where at least one element is missing


######################## Add median income data #####################################
income = []

for index, row in soft.iterrows():
    lon = row['longitude']
    lat = row['latitude']
    response = requests.get("http://www.spatialjusticetest.org/api.php?fLat="\
                            + str(lat) + "&fLon=" + str(lon) + "&sGeo=tract")
    
    data = response.json()  # Convert bytype objects to strings
    income.append(data["income"])
    
soft['Income'] = income
soft.to_csv('Attributes_soft.csv')  







    