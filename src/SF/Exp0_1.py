## Hedonic regression function + diff for 2017-2019

import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from Ttest import Ttest
import matplotlib.pyplot as plot
from pandas import DataFrame

path = "F:/RetrofitPolicy/SF Exp0/"
os.chdir(path)

#df = pd.read_csv('pre1978 soft_wood_single_retrofitted.csv')  # 154 samples
df = pd.read_csv('pre1978 soft_wood_single_noncompliant.csv')   # 17
#df.info()
df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

df2 = pd.read_csv('pre1978_nonsoft_wood_single.csv')  # 498
#df2 = pd.read_csv('post1978_nonsoft_wood_single.csv')  # 258
#df2.info()
df2.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

l1 = len(df['Age'])
l2 = len(df2['Age'])
     
value0 = np.concatenate((np.array(df['Value2010']), np.array(df['Value2011']), np.array(df['Value2012']), \
         np.array(df2['Value2010']), np.array(df2['Value2011']), np.array(df2['Value2012'])), axis=None)       
         
age0 = np.concatenate(((np.array(df['Age'])-9) , (np.array(df['Age'])-8) , (np.array(df['Age'])-7), \
       (np.array(df2['Age'])-9) , (np.array(df2['Age'])-8) , (np.array(df2['Age'])-7)), axis=None)          

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

value1 = np.concatenate((np.array(df['Value2018']) , np.array(df['Value2017']) , np.array(df2['Value2018']), \
         np.array(df2['Value2017'])), axis=None)
       
age1 = np.concatenate(((np.array(df['Age'])-1) , (np.array(df['Age'])-2) , (np.array(df2['Age'])-1), \
       (np.array(df2['Age'])-2)), axis=None) 
                
room1 = np.concatenate((np.array(df['ROOMS']) , np.array(df['ROOMS']) , np.array(df2['ROOMS']), \
        np.array(df2['ROOMS'])), axis=None)
                 
Parea1 = np.concatenate((np.array(df['SQFT']) , np.array(df['SQFT']) , np.array(df2['SQFT']), \
         np.array(df2['SQFT'])), axis=None)*0.092903
                 
CBD1 = np.concatenate((np.array(df['CBD']) , np.array(df['CBD']) , np.array(df2['CBD']), \
            np.array(df2['CBD'])), axis=None)
    
Park1 = np.concatenate((np.array(df['Park']) , np.array(df['Park']) , np.array(df2['Park']), \
              np.array(df2['Park'])), axis=None)

School1 = np.concatenate((np.array(df['School']) , np.array(df['School']) , np.array(df2['School']), \
              np.array(df2['School'])), axis=None)

Police1 = np.concatenate((np.array(df['Police']) , np.array(df['Police']) , np.array(df2['Police']), \
              np.array(df2['Police'])), axis=None)

Fire1 = np.concatenate((np.array(df['Fire']) , np.array(df['Fire']) , np.array(df2['Fire']), \
              np.array(df2['Fire'])), axis=None)   
                 
Income1 = np.concatenate((np.array(df['Income_median']) , np.array(df['Income_median']) , np.array(df2['Income_median']), \
          np.array(df2['Income_median'])), axis=None) 

age = np.concatenate((age0, age1), axis=None)

room = np.concatenate((room023, room1), axis=None)

Parea = np.concatenate((Parea023, Parea1), axis=None)

CBD = np.concatenate((CBD023, CBD1), axis=None)

Park = np.concatenate((Park023, Park1), axis=None)

School = np.concatenate((School023, School1), axis=None)

Police = np.concatenate((Police023, Police1), axis=None)

Fire = np.concatenate((Fire023, Fire1), axis=None)

Income = np.concatenate((Income023, Income1), axis=None)

beta1 = np.concatenate((np.zeros(l1*3+l2*3), np.ones(l1*2+l2*2)), axis=None)

beta2 = np.concatenate((np.ones(l1*3), np.zeros(l2*3), np.ones(l1*2), np.zeros(l2*2)), axis=None)

beta3 = np.concatenate((np.zeros(l1*3+l2*3), np.ones(l1*2), np.zeros(l2*2)), axis=None)

Income = np.log(Income) 

X = np.stack((age, room, Parea, CBD, Park, School, Police, Fire, Income, beta1, beta2, beta3), axis=-1) 

y = np.concatenate((value0, value1), axis=None)

y = np.log(y)

########### calculate correlation matrix #####################################
# z = np.stack((age, room, Parea, CBD, Park, School, Police, Fire, Income, beta1, beta2, beta3, y), axis=-1)

# corMat = DataFrame(z).corr()
                   
# print(corMat)

# plot.pcolor(corMat, cmap='bwr')

# plot.show()

########################### OLS fit ##########################################
reg = LinearRegression().fit(X, y)

reg.score(X, y)    # Return R^2

reg.coef_

reg.intercept_

Y = reg.predict(X)

print(Ttest(reg.intercept_, reg.coef_, X, y, Y))
