## The shortest distance to hazarouds buildings
## The distance to the nearest facilities

import os
import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
from scipy.spatial import distance

# path = "F:/RetrofitPolicy/SF Exp2/"
# os.chdir(path)

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
url ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/raw/SF_Exp1/Soft-Story_Properties20200925.csv'
df = pd.read_csv(url,index_col=False)

url2 = 'https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp1/sales_history_clean.csv'
df2 = pd.read_csv(url2,index_col=False)

hazard_lon = []
hazard_lat = []

for index, row in df.iterrows():

    lon,lat = map(float, row['point'].replace('POINT ','').strip('()').split())
    hazard_lon.append(lon)
    hazard_lat.append(lat)

hazard_nodes = np.stack((hazard_lat, hazard_lon), axis=-1)     

Hazard = []
      
for index, row in df2.iterrows():
    
    lon = row['longitude']
    lat = row['latitude']
    
    property_index = closest_node((lat,lon),hazard_nodes)
    property_dist = haversine(lat, property_index[0], lon, property_index[1])
    Hazard.append(property_dist)  


######################### Central Business District ################################
center_lat = 37.794643 
center_lon = -122.399939

CBD = []

for index, row in df2.iterrows():     
    lon = row['longitude']
    lat = row['latitude']
    dist = haversine(lat, center_lat, lon, center_lon)
    CBD.append(dist)


################################## Facilities #####################################
url3 ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp2/Facilities_SF.csv'
df3 = pd.read_csv(url3,index_col=False)

park_lon = []; school_lon = []; fire_lon = []; police_lon = []
park_lat = []; school_lat = []; fire_lat = []; police_lat = []

for index, row in df3.iterrows():

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
     

park = []; school = []; fire = []; police = []
 
      
for index, row in df2.iterrows():
    
    lon = row['longitude']
    lat = row['latitude']
    
    park_index = closest_node((lat,lon),park_nodes)
    park_dist = haversine(lat, park_index[0], lon, park_index[1])
    park.append(park_dist)  
       
    school_index = closest_node((lat,lon),school_nodes)
    school_dist = haversine(lat, school_index[0], lon, school_index[1])
    school.append(school_dist)    
        
    fire_index = closest_node((lat,lon),fire_nodes)
    fire_dist = haversine(lat, fire_index[0], lon, fire_index[1])
    fire.append(fire_dist)  
        
    police_index = closest_node((lat,lon),police_nodes)
    police_dist = haversine(lat, police_index[0], lon, police_index[1])
    police.append(police_dist)    


d = {'SoftStory':Hazard,'CBD':CBD,'Park':park,'School':school,'Police':police,'Fire':fire}  
df4 = pd.DataFrame(data=d) 
df4 = pd.concat([df2,df4], axis=1)  
df4.to_csv('Attributes.csv')
summary = df4.describe() 
print(summary)   


################### Plot distance histograms ################################
plt.figure(figsize=(20, 10))
plt.subplot(231)
plt.hist(df4['SoftStory'], bins=15)
plt.xlabel('Distance from the nearest soft-story buildings (km)', fontsize=12)
plt.ylabel('Number of single-family houses', fontsize=12)
plt.subplot(232)
plt.hist(df4['CBD'], bins=15)
plt.xlabel('Distance from central business district (km)', fontsize=12)
plt.ylabel('Number of single-family houses', fontsize=12)
plt.subplot(233)
plt.hist(df4['Park'], bins=15)
plt.xlabel('Distance from the nearest park (km)', fontsize=12)
plt.ylabel('Number of single-family houses', fontsize=12)
plt.subplot(234)
plt.hist(df4['School'], bins=15)
plt.xlabel('Distance from the nearest school district (km)', fontsize=12)
plt.ylabel('Number of single-family houses', fontsize=12)
plt.subplot(235)
plt.hist(df4['Police'], bins=15)
plt.xlabel('Distance from the nearest police office (km)', fontsize=12)
plt.ylabel('Number of single-family houses', fontsize=12)
plt.subplot(236)
plt.hist(df4['Fire'], bins=15)
plt.xlabel('Distance from the nearest fire station (km)', fontsize=12)
plt.ylabel('Number of single-family houses', fontsize=12)
plt.show()
    
