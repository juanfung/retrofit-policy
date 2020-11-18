## Hedonic regression function + diff for 2013-2015

import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from math import sqrt
import matplotlib.pyplot as plt
from Ttest import Ttest

path = "F:/RetrofitPolicy/SF Exp0/"
os.chdir(path)

#df = pd.read_csv('pre1978 soft_wood_single_retrofitted.csv')  # 154 samples
df = pd.read_csv('pre1978 soft_wood_single_noncompliant.csv')   # 17
#df.info()
df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

#df2 = pd.read_csv('pre1978_nonsoft_wood_single.csv')  # 498
df2 = pd.read_csv('post1978_nonsoft_wood_single.csv')  # 258
#df2.info()
df2.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

l1 = len(df['Age'])
l2 = len(df2['Age'])

value0 = np.concatenate((np.array(df['Value2010']), np.array(df['Value2011']), np.array(df['Value2012']), \
         np.array(df2['Value2010']), np.array(df2['Value2011']), np.array(df2['Value2012'])), axis=None)       
         
age0 = np.concatenate(((np.array(df['Age'])-9) , (np.array(df['Age'])-8) , (np.array(df['Age'])-7), \
       (np.array(df2['Age'])-9) , (np.array(df2['Age'])-8) , (np.array(df2['Age'])-7)), axis=None) 

value3 = np.concatenate((np.array(df['Value2015']) , np.array(df['Value2014']) , np.array(df['Value2013']), \
         np.array(df2['Value2015']) , np.array(df2['Value2014']) , np.array(df2['Value2013'])), axis=None)
         
age3 = np.concatenate(((np.array(df['Age'])-4) , (np.array(df['Age'])-5) , (np.array(df['Age'])-6), \
       (np.array(df2['Age'])-4) , (np.array(df2['Age'])-5) , (np.array(df2['Age'])-6)), axis=None)         

room023 = np.concatenate((np.array(df['ROOMS']) , np.array(df['ROOMS']) , np.array(df['ROOMS']), \
          np.array(df2['ROOMS']) , np.array(df2['ROOMS']) , np.array(df2['ROOMS'])), axis=None)
              
Parea023 = np.concatenate((np.array(df['SQFT']) , np.array(df['SQFT']) , np.array(df['SQFT']), \
           np.array(df2['SQFT']) , np.array(df2['SQFT']) , np.array(df2['SQFT'])), axis=None)*0.092903
         
CBD023 = np.concatenate((np.array(df['CBD']) , np.array(df['CBD']) , np.array(df['CBD']), \
              np.array(df2['CBD']) , np.array(df2['CBD']) , np.array(df2['CBD'])), axis=None)
    
Park023 = np.concatenate((np.array(df['Park']) , np.array(df['Park']) , np.array(df['Park']), \
              np.array(df2['Park']) , np.array(df2['Park']) , np.array(df2['Park'])), axis=None)

School023 = np.concatenate((np.array(df['School']) , np.array(df['School']) , np.array(df['School']), \
              np.array(df2['School']) , np.array(df2['School']) , np.array(df2['School'])), axis=None)

Police023 = np.concatenate((np.array(df['Police']) , np.array(df['Police']) , np.array(df['Police']), \
              np.array(df2['Police']) , np.array(df2['Police']) , np.array(df2['Police'])), axis=None)

Fire023 = np.concatenate((np.array(df['Fire']) , np.array(df['Fire']) , np.array(df['Fire']), \
              np.array(df2['Fire']) , np.array(df2['Fire']) , np.array(df2['Fire'])), axis=None)
                
Income023 = np.concatenate((np.array(df['Income_median']) , np.array(df['Income_median']) , np.array(df['Income_median']), \
            np.array(df2['Income_median']) , np.array(df2['Income_median']) , np.array(df2['Income_median'])), axis=None)
         
Income023 = np.log(Income023) 

age = np.concatenate((age0, age3), axis=None)

room = np.concatenate((room023, room023), axis=None)

Parea = np.concatenate((Parea023, Parea023), axis=None)

CBD = np.concatenate((CBD023, CBD023), axis=None)

Park = np.concatenate((Park023, Park023), axis=None)

School = np.concatenate((School023, School023), axis=None)

Police = np.concatenate((Police023, Police023), axis=None)

Fire = np.concatenate((Fire023, Fire023), axis=None)

Income = np.concatenate((Income023, Income023), axis=None)

beta1 = np.concatenate((np.zeros(l1*3+l2*3), np.ones(l1*3+l2*3)), axis=None)

beta2 = np.concatenate((np.ones(l1*3), np.zeros(l2*3), np.ones(l1*3), np.zeros(l2*3)), axis=None)

beta3 = np.concatenate((np.zeros(l1*3+l2*3), np.ones(l1*3), np.zeros(l2*3)), axis=None)

X = np.stack((age, room, Parea, CBD, Park, School, Police, Fire, Income, beta1, beta2, beta3), axis=-1) 

y = np.concatenate((value0, value3), axis=None)

y = np.log(y)

#reg = Ridge(alpha=0.001).fit(X,y)
#
reg = LinearRegression().fit(X,y)

reg.score(X, y)  # Return R^2

reg.coef_

reg.intercept_

Y = reg.predict(X)

print(Ttest(reg.intercept_, reg.coef_, X, y, Y))


################### Plot real vs. prediction ##################################
# len = np.size(y)
# t = np.arange(len)
# fig = plt.figure(figsize=(10, 3.5))
# ax1 = fig.add_subplot(111)

# ax1.scatter(t, y, s=6, c='k', marker="s", label='True')
# ax1.scatter(t, Y, s=6, c='r', marker="o", label='Prediction')
# plt.xlabel('Number of properties', fontsize=12)
# plt.ylabel('Logrithm of sale price ($)', fontsize=12)
# plt.legend(loc='upper left', fontsize=12)
# plt.show()

################### Plot actual vs. predicted 45 degree ########################
# plt.figure(figsize=(5, 4))
# plt.scatter(Y, y, s=4, label='True')
# plt.xlim(9,17)
# plt.ylim(9,17)
# plt.xlabel('Predicted logarithm of sale price ($)', fontsize=12)
# plt.ylabel('Actual logarithm of sale price ($)', fontsize=12)
# plt.show()

################### Plot actual vs. predicted histogram ########################
# diff = Y - y 

# plt.figure(figsize=(5, 4))
# plt.hist(diff, bins = 40)
# plt.xlabel('Prediction error ($)', fontsize=12)
# plt.ylabel('Frequency', fontsize=12)
# plt.show()


################### Plot attributes vs. y #####################################
# plt.figure(figsize=(20, 15))

# plt.subplot(431)
# plt.scatter(X[:,0], y, s=10)
# plt.xlabel('Building age', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(432)
# plt.scatter(X[:,1], y, s=10)
# plt.xlabel('Number of rooms', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(433)
# plt.scatter(X[:,2], y, s=10)
# plt.xlabel('Property area (m\u00b2)', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(434)
# plt.scatter(X[:,3], y, s=10)
# plt.xlabel('Distance from central business district (km)', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(435)
# plt.scatter(X[:,4], y, s=10)
# plt.xlabel('Distance from the nearest park (km)', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(436)
# plt.scatter(X[:,5], y, s=10)
# plt.xlabel('Distance from the nearest school district (km)', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(437)
# plt.scatter(X[:,6], y, s=10)
# plt.xlabel('Distance from the nearest police office (km)', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(438)
# plt.scatter(X[:,7], y, s=10)
# plt.xlabel('Distance from the nearest fire station (km)', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(439)
# plt.scatter(X[:,8], y, s=10)
# plt.xlabel('Logarithm of median household income ($)', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(4,3,10)
# plt.scatter(X[:,9], y, s=10)
# plt.xlabel('D\u209C', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(4,3,11)
# plt.scatter(X[:,10], y, s=10)
# plt.xlabel('D\u2097', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)
# plt.subplot(4,3,12)
# plt.scatter(X[:,11], y, s=10)
# plt.xlabel('D\u209C*D\u2097', fontsize=12)
# plt.ylabel('Logarithm of sale price ($)', fontsize=12)

# plt.show()


############################ Cross Validation #################################
# indices = range(len(X))
# xTest = [X[i] for i in indices if i%3 == 0]
# xTrain = [X[i] for i in indices if i%3 != 0]
# yTest = [y[i] for i in indices if i%3 == 0]
# yTrain = [y[i] for i in indices if i%3 != 0]

# alphaList = [0.1**i for i in [0,1,2,3,4,5,6]]

# rmsError = []
# for alph in alphaList:
#     Model = Ridge(alpha=alph)
#     Model.fit(xTrain, yTrain)
#     rmsError.append(np.linalg.norm((yTest - Model.predict(xTest)),2)/sqrt(len(yTest)))
    
# print("RMS Error           alpha")
# for i in range(len(rmsError)):
#     print(rmsError[i], alphaList[i])










