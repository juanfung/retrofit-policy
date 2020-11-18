## Retrive Census data from Justice Map API

import os
import requests
import pandas as pd
import time 
import numpy as np

# path = "F:/RetrofitPolicy/SF Exp2/"
# os.chdir(path)

###################################################################################
url ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp2/Attributes.csv'
df = pd.read_csv(url,index_col=0)

income = []
for index, row in df.iloc[0:7000].iterrows():
    lon = row['longitude']
    lat = row['latitude']
    response = requests.get("http://www.spatialjusticetest.org/api.php?fLat="\
                            + str(lat) + "&fLon=" + str(lon) + "&sGeo=tract")
    
    # print(response.status_code)
    # print(response.content)
    data = response.json()  # Convert bytype objects to strings
    # print(data)
    income.append(data["income"])
   
time.sleep(600)

income2 = []    
for index, row in df.iloc[7000:14000].iterrows():
    lon = row['longitude']
    lat = row['latitude']
    response = requests.get("http://www.spatialjusticetest.org/api.php?fLat="\
                            + str(lat) + "&fLon=" + str(lon) + "&sGeo=tract")
    data = response.json()
    income2.append(data["income"])
    

time.sleep(600)
 
income3 = []    
for index, row in df.iloc[14000:len(df)].iterrows():
    lon = row['longitude']
    lat = row['latitude']
    response = requests.get("http://www.spatialjusticetest.org/api.php?fLat="\
                            + str(lat) + "&fLon=" + str(lon) + "&sGeo=tract")
    data = response.json()
    income3.append(data["income"])


income = np.concatenate([income,income2,income3], axis=None)
df['Income'] = income
df.to_csv('Attributes.csv')


    
    
    
