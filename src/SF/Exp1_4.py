## Retrive Census data from Justice Map API

import os
import requests
import pandas as pd
import time 
import numpy as np

path = "F:/RetrofitPolicy/SF Exp1/"
os.chdir(path)

###################################################################################
url ='Attributes_soft.csv'
df = pd.read_csv(url,index_col=0)
income = []
for index, row in df.iterrows():
    lon = row['longitude']
    lat = row['latitude']
    response = requests.get("http://www.spatialjusticetest.org/api.php?fLat="\
                            + str(lat) + "&fLon=" + str(lon) + "&sGeo=tract")
    
    # print(response.status_code)
    # print(response.content)
    data = response.json()  # Convert bytype objects to strings
    # print(data)
    income.append(data["income"])

df['Income'] = income
df.to_csv('Attributes_soft.csv')   


url2 ='Attributes_pre1980wood.csv'
df2 = pd.read_csv(url2,index_col=0)
income2 = []    
for index, row in df2.iterrows():
    lon = row['longitude']
    lat = row['latitude']
    response = requests.get("http://www.spatialjusticetest.org/api.php?fLat="\
                            + str(lat) + "&fLon=" + str(lon) + "&sGeo=tract")
    data = response.json()
    income2.append(data["income"])
    
df2['Income'] = income2
df2.to_csv('Attributes_pre1980wood.csv')


url3 ='Attributes_post1980wood.csv'
df3 = pd.read_csv(url3,index_col=0) 
income3 = []    
for index, row in df3.iterrows():
    lon = row['longitude']
    lat = row['latitude']
    response = requests.get("http://www.spatialjusticetest.org/api.php?fLat="\
                            + str(lat) + "&fLon=" + str(lon) + "&sGeo=tract")
    data = response.json()
    income3.append(data["income"])

df3['Income'] = income3
df3.to_csv('Attributes_post1980wood.csv')

