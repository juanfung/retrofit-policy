# Determine the threshold of distance
# Method 1. Look at the distance when its coefficient in the Hedonic regression function approaches 0
# Method 2. Look at the distance when the Pearson correlation coefficient approaches 0

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# path = "F:/RetrofitPolicy/SF Exp2/"
# os.chdir(path)

url ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp2/Attributes.csv'
df = pd.read_csv(url,index_col=0)
# df = df[df['Bed'] <= 10]  # Remove single-family homes with more than 10 bedrooms

df.sort_values('SoftStory')  # Sort data by the distance to soft-story buildings

Year = 2020
age = Year - np.array(df['YRBLT'])

bed = np.array(df['Bed'])

bath = np.array(df['Bath'])

Parea = np.array(df['SQFT'])*0.092903

CBD = np.array(df['CBD'])
    
Park = np.array(df['Park'])

School = np.array(df['School'])

Police = np.array(df['Police'])

Fire = np.array(df['Fire'])

Hazard = np.array(df['SoftStory'])

Income = np.array(df['Income'])
Income = np.log(Income) 

value = np.array(df['Sale_price_adj'])
Y = np.log(value)

##################################### Method 1 ###########################################
X = np.stack((age, bed, bath, Parea, Park, School, Police, Fire, Hazard, Income), axis=-1)

coefficient = []

for i in range(20):
    x = X[int(round(len(X)/20*i)) : int(round(len(X)/20*(i+1)))]  # 20 sections
    y = Y[int(round(len(Y)/20*i)) : int(round(len(Y)/20*(i+1)))]  # 20 Hedonic regrssion functions
    reg = LinearRegression().fit(x, y)    
    coefficient.append(reg.coef_[8])
    

distance = df['SoftStory'].quantile([.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,\
                                      .6,.65,.7,.75,.8,.85,.9,.95,1])
    
threshold1 = distance.iloc[coefficient.index(min(np.absolute(coefficient)))]
print('The threshold is %f km.' % threshold1)

plt.figure(figsize=(5, 4))
plt.scatter(distance, coefficient, s=4, label='True')
plt.xlabel('Shortest distance from soft-story buildings (km)', fontsize=12)
plt.ylabel('Coefficient', fontsize=12)
plt.show()

## The threshold is 0.088825 km.

################################### Method 2 ############################################
correlation = []

for j in range(20):
    x = Hazard[int(round(len(Hazard)/20*j)) : int(round(len(Hazard)/20*(j+1)))]   # 20 sections
    y = Y[int(round(len(Y)/20*j)) : int(round(len(Y)/20*(j+1)))]   # 20 correlation coefficients
    cor =  np.corrcoef(x,y)
    correlation.append(cor[0,1])

# distance = df['SoftStory'].quantile([.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,\
#                                       .6,.65,.7,.75,.8,.85,.9,.95,1])
try:
    threshold2 = distance.iloc[correlation.index(min(np.absolute(correlation)))]
except ValueError:
    threshold2 = distance.iloc[correlation.index(-min(np.absolute(correlation)))]

print('The threshold is %f km.' % threshold2)

plt.figure(figsize=(5, 4))
plt.scatter(distance, correlation, s=4, label='True')
plt.xlabel('Shortest distance from soft-story buildings (km)', fontsize=12)
plt.ylabel('Correlation', fontsize=12)
plt.show()

## The threshold is 0.088825 km.


