## Hedonic regression function + diff for 2015-2017


import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from Ttest import Ttest

#df = pd.read_csv('D:/RetrofitPolicy/pre1978 soft_wood_single_retrofitted.csv')  # 154 samples
df = pd.read_csv('D:/RetrofitPolicy/pre1978 soft_wood_single_noncompliant.csv')   # 17
#df.info()
df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

#df2 = pd.read_csv('D:/RetrofitPolicy/pre1978_nonsoft_wood_single.csv')  # 498
df2 = pd.read_csv('D:/RetrofitPolicy/post1978_nonsoft_wood_single.csv')  # 258
#df2.info()
df2.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

l1 = len(df['Age'])
l2 = len(df2['Age'])

value0 = np.concatenate((np.array(df['Value2010']), np.array(df['Value2011']), np.array(df['Value2012']), \
         np.array(df2['Value2010']), np.array(df2['Value2011']), np.array(df2['Value2012'])), axis=None)       
         
age0 = np.concatenate(((np.array(df['Age'])-9) , (np.array(df['Age'])-8) , (np.array(df['Age'])-7), \
       (np.array(df2['Age'])-9) , (np.array(df2['Age'])-8) , (np.array(df2['Age'])-7)), axis=None) 

value2 = np.concatenate((np.array(df['Value2017']) , np.array(df['Value2016']) , np.array(df['Value2015']), \
         np.array(df2['Value2017']) , np.array(df2['Value2016']) , np.array(df2['Value2015'])), axis=None)
        
age2 = np.concatenate(((np.array(df['Age'])-2) , (np.array(df['Age'])-3) , (np.array(df['Age'])-4), \
       (np.array(df2['Age'])-2) , (np.array(df2['Age'])-3) , (np.array(df2['Age'])-4)), axis=None)

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

age = np.concatenate((age0, age2), axis=None)

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

y = np.concatenate((value0, value2), axis=None)

y = np.log(y)

reg = LinearRegression().fit(X, y)

reg.score(X, y)    # Return the coefficient of determination R^2 of the prediction.

reg.coef_

reg.intercept_

Y = reg.predict(X)

print(Ttest(reg.intercept_, reg.coef_, X, y, Y))