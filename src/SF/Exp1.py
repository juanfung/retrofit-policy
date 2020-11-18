# Soft-story buildings
# 1. Add building characteristics
# 2. Check compliance status for condos
# 3. Add sales data, convert sales data to 2019 USD
# 4. Add assessor data, convert assessor data to 2019 USD

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# path = "F:/RetrofitPolicy/SF Exp1/"
# os.chdir(path)

##################################### Functions ############################################# 
## Convert sales and assessor data to 2019 USD

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
            value.append(Estimate[-2])  # In case that assessor data is not available
        
    return  round(value,1)


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
            value.append(Estimate)  # In case that assessor data is not available
        
    return round(value,1) 

################################################################################

## Add building characteristics
url ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/raw/SF_Exp1/Soft-Story_Properties20200925.csv'
df = pd.read_csv(url,index_col=False)

url2 = 'https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/raw/SF_Exp1/Assessor%20data/SF_property_tax2017-2018.csv'
df2 = pd.read_csv(url2,index_col=False)

df['Block'] = df['Block'].astype(str)
df2['Block'] = df2['Block'].astype(str)
df['Lot'] = df['Lot'].astype(str)
df2['Lot'] = df2['Lot'].astype(str)
df3 = pd.merge(df, df2, how='left', on=['Block', 'Lot'])



## Add building use categories
url4 ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/raw/SF_Exp1/Assessor%20data/Class_code.csv'
df4 = pd.read_csv(url4,index_col=0)

use = []
use_missing = 0
    
for index, row in df3.iterrows():
    try:
        description = df4.loc[df4.CODE==row['RP1CLACDE'], 'DESCRIPTION'].values[0]
        use.append(description)
    except IndexError:
        use.append(np.nan)
        use_missing += 1
   
df3['Use'] = use
df3.to_csv('Soft_story.csv')


## Statistics of buildings
use_list = list(set(use))  # Extract building categories
use_count = []

for item in use_list:
   use_count.append(use.count(item))

y = np.arange(len(use_list))

plt.bar(y, use_count, align='center', alpha=0.5)
plt.xticks(y,use_list,rotation=90)
plt.xlabel('Usage', fontsize=12)
plt.ylabel('Number of buildings', fontsize=12)
plt.show()


## Compliance status of single-family houses
options = ['Condominium','Dwelling']
compliance = df3.loc[df3['Use'].isin(options),'status']
status_list = list(set(compliance))  # Extract building categories
status_def_list = compliance.tolist()
status_count = []

for item in status_list:
   status_count.append(status_def_list.count(item))

y = np.arange(len(status_list))

plt.bar(y, status_count, align='center', alpha=0.5)
plt.xticks(y,status_list,rotation=90)
plt.xlabel('Compliance status for single-family houses', fontsize=12)
plt.ylabel('Number of buildings', fontsize=12)
plt.show()


## Export data for retrofitted and noncompliant soft-story buildings to csv files
soft_retrofitted = df3[df3['Use'].isin(options) & (df3['status']=='Work Complete, CFC Issued')]
options2 = ['Non-Compliant','Permit Submitted, CFC Required by 9/15/2020']
soft_noncompliant = df3[df3['Use'].isin(options) & df3['status'].isin(options2)]

soft_retrofitted.to_csv('SoftStroy_single_retrofitted.csv')
soft_noncompliant.to_csv('SoftStory_single_noncompliant.csv')


## Add sales data
url5 ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp1/Soft%20story/sales%20soft%20story%20clean.csv'
df5 = pd.read_csv(url5,index_col=False)

df5 = df5[['apn','amount.saleAmt','Sale_year']]
df3 = pd.merge(df5, df3, how='left', left_on='apn', right_on='RP1PRCLID')


## Convert sales data to 2019 USD        
value1 = convertor(df3,'amount.saleAmt','Sale_year')
df3['Sale_price_2019'] = value1
df3.to_csv('SoftStory_sales.csv')
df3 = df3[df3['status'].notna()]
df3.to_csv('SoftStory_sales_clean.csv')

## Add assessor data
for y in range(2008,2019,1):
    url6 = 'https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/\
    raw/SF_Exp1/Assessor%20data/SF_property_tax'+str(y-1)+'-'+str(y)+'.csv'
    df6 = pd.read_csv(url6,index_col=False)
    
    assessed_value = df6['RP1IMPVAL'] + df6['RP1LNDVAL']
    df6[str(y)] = assessed_value
    df6 = df6[['RP1PRCLID',str(y)]]
    
    soft_retrofitted = pd.merge(soft_retrofitted, df6, how='left', on='RP1PRCLID')
    soft_noncompliant = pd.merge(soft_noncompliant, df6, how='left', on='RP1PRCLID')

    
## Convert assessor data to 2019 USD  
value2 = convertor2(soft_retrofitted, 2008, 2018)
df7 = pd.concat(value2, axis=1).T   # Convert list of pd series to pd frame

value3 = convertor2(soft_noncompliant, 2008, 2018)
df8 = pd.concat(value3, axis=1).T

soft_retrofitted = pd.concat([soft_retrofitted, df7], axis=1)
soft_noncompliant = pd.concat([soft_noncompliant,df8], axis=1)
soft_retrofitted.to_csv('SoftStory_assessment_retrofitted.csv')
soft_noncompliant.to_csv('SoftStory_assessment_noncompliant.csv')

df7.dropna(how='any', inplace=True)  # Drop the rows where at least one element is missing
df7[(df7 != 0).all(1)]  # Drop the rows containing 0
df8.dropna(how='any', inplace=True)
df8[(df8 != 0).all(1)]

summary_retrofitted = df7.describe()
print(summary_retrofitted)
summary_noncompliant = df8.describe()
print(summary_noncompliant)


fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.errorbar(range(2008,2019,1), summary_retrofitted.iloc[1,:11],\
             summary_retrofitted.iloc[2,:11], linestyle='None', marker='_')
ax1.errorbar(range(2008,2019,1), summary_noncompliant.iloc[1,:11],\
             summary_noncompliant.iloc[2,:11], linestyle='None', marker='_')
ax1.legend(['Retrofitted','Noncompliant'], fontsize=12)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Assessed property value (2019 USD)', fontsize=12)
plt.show() 
  
