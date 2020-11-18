# Post-1980 wood-frame buildings
# 1. Add building characteristics
# 2. Add sales data, convert sales data to 2019 USD
# 3. Add assessor data, convert assessor data to 2019 USD

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# path = "F:/RetrofitPolicy/SF Exp1/"
# os.chdir(path)

################################ Functions ####################################
url_inflation ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/raw/SF_Exp1/CPI.csv'
df_inflation = pd.read_csv(url,index_col=0)

# df_inflation = pd.read_csv('CPI.csv')

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
            value.append(Estimate[-2])  # Assessor data is not available
        
    return  value


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
            value.append(Estimate)  # Assessor data is not available
        
    return value 

################################################################################

## Add building characteristics
url ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp1/Wood%20frame/post1980_nonsoft_wood_single.csv'
df = pd.read_csv(url,index_col=False)

url2 = 'https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/raw/SF_Exp1/Assessor%20data/SF_property_tax2017-2018.csv'
df2 = pd.read_csv(url2,index_col=False)

# df = pd.read_csv('post1980_nonsoft_wood_single.csv')
# df2 = pd.read_csv('Assessor data/SF_property_tax2017-2018.csv')

df['Block'] = df['Block'].astype(str)
df2['Block'] = df2['Block'].astype(str)
df['Lot'] = df['Lot'].astype(str)
df2['Lot'] = df2['Lot'].astype(str)
df3 = pd.merge(df, df2, how='left', on=['Block', 'Lot'])


## Add building use categories
url4 ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/raw/SF_Exp1/Assessor%20data/Class_code.csv'
df4 = pd.read_csv(url4,index_col=0)

# df4 = pd.read_csv('Assessor data/Class_code.csv')

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

## Statistics of buildings
use_list = list(set(use))
use_count = []

for item in use_list:
   use_count.append(use.count(item))

y = np.arange(len(use_list))

plt.bar(y, use_count, align='center', alpha=0.5)
plt.xticks(y,use_list,rotation=90)
plt.xlabel('Usage', fontsize=12)
plt.ylabel('Number of buildings', fontsize=12)
plt.show()


## Add sales data
url5 ='https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/processed/SF_Exp1/sales_history_clean.csv'
df5 = pd.read_csv(url5,index_col=0,parse_dates=[0])

# df5 = pd.read_csv('sales_history_clean.csv')

df5 = df5[['APN','Sale_price','Sale_year']]
df3 = pd.merge(df3, df5, how='left',left_on='RP1PRCLID', right_on='APN')


## Convert sales data to 2019 USD        
value1 = convertor(df3,'Sale_price','Sale_year')
df3['Sale_price_2019'] = value1
df3.to_csv('Post1980_woodframe.csv')  # Export data to a csv file 


## Add assessor data
for y in range(2008,2019,1):
    url6 = 'https://raw.githubusercontent.com/juanfung/retrofit-policy/master/data/\
    raw/SF_Exp1/Assessor%20data/SF_property_tax'+str(y-1)+'-'+str(y)+'.csv'
    df6 = pd.read_csv(url6,index_col=False)
    
    # df6 = pd.read_csv('Assessor data/SF_property_tax'+str(y-1)+'-'+str(y)+'.csv')
    
    assessed_value = df6['RP1IMPVAL'] + df6['RP1LNDVAL']
    df6[str(y)] = assessed_value
    df6 = df6[['RP1PRCLID',str(y)]]
    
    df3 = pd.merge(df3, df6, how='left', on='RP1PRCLID')


## Convert assessor data to 2019 USD  
value2 = convertor2(df3, 2008, 2018)
df7 = pd.concat(value2, axis=1).T   # Convert list of pd series to pd frame
df3 = pd.concat([df3, df7], axis=1)
df3.to_csv('Wood_assessment_post1980.csv')   # Export data to a csv file 

df7.dropna(how='any', inplace=True)  # Drop the rows where at least one element is missing
df7[(df7 != 0).all(1)]  # Drop the rows containing 0
summary = df7.describe()
print(summary)

plt.errorbar(range(2008,2019,1), summary.iloc[1,:11],\
             summary.iloc[2,:11], linestyle='None', marker='_')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Assessed property value (2019 USD)', fontsize=12)
plt.show()
    
