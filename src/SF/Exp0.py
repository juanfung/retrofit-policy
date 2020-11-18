## Statistics for variables used in the Hedonic model


import pandas as pd
import numpy as np
import os

path = "F:/RetrofitPolicy/SF Exp0/"
os.chdir(path)

#df = pd.read_csv('pre1978 soft_wood_single_retrofitted.csv')
df = pd.read_csv('pre1978 soft_wood_single_noncompliant.csv')


# df[['Age','ROOMS','SQFT']].describe()
# df[['UnitPrice','CBD', 'Park','School']].describe()
# df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
# df[['Police','Fire','Income_median','Value2018']].describe()


#df2 = pd.read_csv('pre1978_nonsoft_wood_single.csv')
df2 = pd.read_csv('post1978_nonsoft_wood_single.csv')

# df2.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
# df2[['Age','ROOMS','SQFT']].describe()
# df2[['UnitPrice','CBD', 'Park','School']].describe()
# df2[['Police','Fire','Income_median','Value2018']].describe()


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

value2 = np.concatenate((np.array(df['Value2017']) , np.array(df['Value2016']) , np.array(df['Value2015']), \
         np.array(df2['Value2017']) , np.array(df2['Value2016']) , np.array(df2['Value2015'])), axis=None)
        
age2 = np.concatenate(((np.array(df['Age'])-2) , (np.array(df['Age'])-3) , (np.array(df['Age'])-4), \
       (np.array(df2['Age'])-2) , (np.array(df2['Age'])-3) , (np.array(df2['Age'])-4)), axis=None)

value3 = np.concatenate((np.array(df['Value2015']) , np.array(df['Value2014']) , np.array(df['Value2013']), \
         np.array(df2['Value2015']) , np.array(df2['Value2014']) , np.array(df2['Value2013'])), axis=None)
         
age3 = np.concatenate(((np.array(df['Age'])-4) , (np.array(df['Age'])-5) , (np.array(df['Age'])-6), \
       (np.array(df2['Age'])-4) , (np.array(df2['Age'])-5) , (np.array(df2['Age'])-6)), axis=None)   

age = np.concatenate((age0, age1), axis=None)
print("age: ", np.mean(age), np.std(age), np.min(age), np.max(age))

room = np.concatenate((room023, room023), axis=None)
print("room: ", np.mean(room), np.std(room), np.min(room), np.max(room))

Parea = np.concatenate((Parea023, Parea023), axis=None)
print("Prop area: ", np.mean(Parea), np.std(Parea), np.min(Parea), np.max(Parea))

CBD = np.concatenate((CBD023, CBD023), axis=None)
print("CBD: ", np.mean(CBD), np.std(CBD), np.min(CBD), np.max(CBD))

Park = np.concatenate((Park023, Park023), axis=None)
print("Park: ", np.mean(Park), np.std(Park), np.min(Park), np.max(Park))

School = np.concatenate((School023, School023), axis=None)
print("School: ", np.mean(School), np.std(School), np.min(School), np.max(School))

Police = np.concatenate((Police023, Police023), axis=None)
print("Police: ", np.mean(Police), np.std(Police), np.min(Police), np.max(Police))

Fire = np.concatenate((Fire023, Fire023), axis=None)
print("Fire: ", np.mean(Fire), np.std(Fire), np.min(Fire), np.max(Fire))

Income = np.concatenate((Income023, Income023), axis=None)
print("Income: ", np.mean(Income), np.std(Income), np.min(Income), np.max(Income))

D1 = np.concatenate((np.zeros(l1*3+l2*3), np.ones(l1*2+l2*2)), axis=None)
print("D1: ", np.mean(D1), np.std(D1), np.min(D1), np.max(D1))

D2 = np.concatenate((np.ones(l1*3), np.zeros(l2*3), np.ones(l1*2), np.zeros(l2*2)), axis=None)
print("D2: ", np.mean(D2), np.std(D2), np.min(D2), np.max(D2))

D3 = np.concatenate((np.zeros(l1*3+l2*3), np.ones(l1*2), np.zeros(l2*2)), axis=None)
print("D3: ", np.mean(D3), np.std(D3), np.min(D3), np.max(D3))

y = np.concatenate((value0, value1), axis=None)
print("price: ", np.mean(y), np.std(y), np.min(y), np.max(y))



