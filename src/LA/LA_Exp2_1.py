## Add sales data, convert sale prices to 2019 USD
## Add assessor data, convert assessed values to 2019 USD

import os
import requests
import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
from scipy.spatial import distance

path = "F:/RetrofitPolicy/LA/" 
os.chdir(path)

################################## Functions #####################################
url_inflation ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/raw/SF_Exp1/CPI.csv'
df_inflation = pd.read_csv(url_inflation,index_col=0)

CPI = df_inflation['Annual']
CPI_matrix = np.tile(CPI,(21,1))
CPI_matrix2 = np.transpose(CPI_matrix)

inflation = CPI_matrix/CPI_matrix2

def convertor(dataframe,column_price,column_year):
    value = [] 
    
    for index, row in dataframe.iterrows():
        Estimate = np.repeat(row[str(column_price)],21)
        try:
            year = int(row[str(column_year)])  
            Estimate = Estimate * inflation[year-2000]
            value.append(Estimate[-2])
        except ValueError:
            value.append(Estimate[-2])
        
    return value


def convertor2(dataframe,year_begin,year_end):
    value = [] 
    
    price = dataframe[str(year_begin)]
    
    for year in range(year_begin+1, year_end+1, 1):
        price = pd.concat([price,dataframe[str(year)]], axis=1)
    
    for index, row in price.iterrows():               
        try:
            Estimate = row * inflation[(year_begin-2000):(year_end-2000+1),19]
            value.append(Estimate)
        except ValueError:
            value.append(Estimate)
        
    return value


####################### Convert sales price to 2019 USD ###############################
df = pd.read_csv('Attributes.csv')
df['Sale_year'] = pd.DatetimeIndex(df['Sale_date']).year
df = df[df.Sale_year < 2020]
value1 = convertor(df,'Sale_price','Sale_year')
df['Sale_price_2019'] = value1
df.to_csv('Attributes.csv')