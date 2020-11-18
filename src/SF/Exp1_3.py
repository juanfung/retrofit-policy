## Distance to city facilities

import os
import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
from scipy.spatial import distance

path = "F:/RetrofitPolicy/SF Exp1/"
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
    
url ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp1/Soft%20story/SoftStory_sales_clean.csv'
df = pd.read_csv(url,index_col=False)    # soft-story 

url2 = 'https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp0/pre1978_nonsoft_wood_single.csv'
df2 = pd.read_csv(url2,index_col=False)    # pre-1980 wood-frame

url3 = 'single family/post1978_nonsoft_wood_single.csv'
df3 = pd.read_csv(url3,index_col=False)    # post-1980 wood-frame 

CBD_soft = []  # Central business district
CBD_pre1980wood = []
CBD_post1980wood = []

center_lat = 37.794643 
center_lon = -122.399939

LON = []; LAT = [] 
for index, row in df.iterrows():     
    lon,lat = map(float, row['point'].replace('POINT ','').strip('()').split())
    LON.append(lon)
    LAT.append(lat)
    dist = haversine(lat, center_lat, lon, center_lon)
    CBD_soft.append(dist)

LON2 = []; LAT2 = [] 
for index, row in df2.iterrows():
    lon,lat = map(float, row['Point'].split())
    LON2.append(lon)
    LAT2.append(lat)
    dist = haversine(lat, center_lat, lon, center_lon)
    CBD_pre1980wood.append(dist)

LON3 = []; LAT3 = []
for index, row in df3.iterrows():
    lon,lat = map(float, row['Point'].split())
    LON3.append(lon)
    LAT3.append(lat)
    dist = haversine(lat, center_lat, lon, center_lon)
    CBD_post1980wood.append(dist)
    
################################## Facilities #####################################
url4 ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp2/Facilities_SF.csv'
df4 = pd.read_csv(url4,index_col=False)

park_lon = []; school_lon = []; fire_lon = []; police_lon = []
park_lat = []; school_lat = []; fire_lat = []; police_lat = []

for index, row in df4.iterrows():

    if row['facilities'] == 'Recreation And Parks':
        park_lon.append(row['longitude'])
        park_lat.append(row['latitude'])
    
    if row['facilities'] == 'School District (Sfusd)':       
        school_lon.append(row['longitude'])
        school_lat.append(row['latitude'])

    if row['facilities'] == 'Fire Department':       
        fire_lon.append(row['longitude'])
        fire_lat.append(row['latitude'])
      
    if row['facilities'] == 'Police Department':       
        police_lon.append(row['longitude'])
        police_lat.append(row['latitude'])


park_nodes = np.stack((park_lat, park_lon), axis=-1)
school_nodes = np.stack((school_lat, school_lon), axis=-1)
fire_nodes = np.stack((fire_lat, fire_lon), axis=-1)
police_nodes = np.stack((police_lat, police_lon), axis=-1)   
     


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


soft = distance_facilities(LON, LAT)
soft['CBD'] = CBD_soft
soft['longitude'] = LON
soft['latitude'] = LAT
soft = pd.concat([soft,df], axis=1)
soft.to_csv('Attributes_soft.csv')
     
pre1980wood = distance_facilities(LON2, LAT2) 
pre1980wood['CBD'] = CBD_pre1980wood 
pre1980wood['longitude'] = LON2
pre1980wood['latitude'] = LAT2
pre1980wood = pd.concat([pre1980wood,df2], axis=1) 
pre1980wood.to_csv('Attributes_pre1980wood.csv')
    
post1980wood = distance_facilities(LON3, LAT3)
post1980wood['CBD'] = CBD_post1980wood 
post1980wood['longitude'] = LON3
post1980wood['latitude'] = LAT3
post1980wood = pd.concat([post1980wood,df3], axis=1) 
post1980wood.to_csv('Attributes_post1980wood.csv')


