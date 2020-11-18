## The shortest distance to hazardous buildings
## The distance to the nearest facilities

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


############################# Hazarodus Buildings #################################
url = 'SoftStory_single.csv'  # Condos
df = pd.read_csv(url,index_col=False)

url2 = 'SoftStory_apartment_list_clean.csv'  # Apartments
df2 = pd.read_csv(url2,index_col=False)

url3 = 'Assessor data LA city/Property_tax2019.csv'
df3 = pd.read_csv(url3, index_col=0)

df4 = pd.merge(df3, df2, how='right', left_on='AIN', right_on='APN')
df4.dropna(how='any', inplace=True)   # Drop rows with missing data
df5 = pd.concat([df, df4], axis=0)


for index, row in df5.iterrows():

    hazard_lon = df5['CENTER_LON'].to_numpy()
    hazard_lat = df5['CENTER_LAT'].to_numpy()

hazard_nodes = np.stack((hazard_lat, hazard_lon), axis=-1)     

Hazard = []

url6 = 'sales_history_clean.csv'
df6 = pd.read_csv(url6,index_col=False)
     
for index, row in df6.iterrows():
    
    lon = row['longitude']
    lat = row['latitude']
    
    property_index = closest_node((lat,lon),hazard_nodes)
    property_dist = haversine(lat, property_index[0], lon, property_index[1])
    Hazard.append(property_dist)  


######################### Central Business District ################################
center_lat = 34.051001
center_lon = -118.257040

CBD = []

for index, row in df6.iterrows():     
    lon = row['longitude']
    lat = row['latitude']
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


LON = df6['longitude'].to_numpy()
LAT = df6['latitude'].to_numpy()
d = distance_facilities(LON, LAT)
df6 = pd.concat([df6,d], axis=1)
df6['CBD'] = CBD
df6.to_csv('Attributes.csv') 

######################## Add median income data #####################################
income = []

for index, row in df6.iloc[58027:58583].iterrows():
    lon = row['longitude']
    lat = row['latitude']
    response = requests.get("http://www.spatialjusticetest.org/api.php?fLat="\
                            + str(lat) + "&fLon=" + str(lon) + "&sGeo=tract")
    
    data = response.json()  # Convert bytype objects to strings
    income.append(data["income"])
    
df6['Income'] = income
df6.to_csv('Attributes.csv')  



