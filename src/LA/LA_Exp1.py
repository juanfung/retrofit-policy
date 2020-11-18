# Soft-story buildings
# 1. Add building characteristics
# 2. Add sales data, convert sales data to 2019 USD
# 3. Add assessor data, convert assessor data to 2019 USD

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = "F:/RetrofitPolicy/LA/" 
os.chdir(path)

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
        
    return  value


def convertor2(dataframe,year_begin,year_end):
    value = [] 
    
    price = dataframe[str(year_begin)]
    
    for year in range(year_begin+1, year_end+1, 1):
        price = pd.concat([price,dataframe[str(year)]], axis=1) # Column names '2019','2018',...
        
    for index, row in price.iterrows():               
        try:
            Estimate = row * inflation[(year_begin-2000):(year_end-2000+1),19]
            value.append(Estimate)
        except ValueError:
            value.append(Estimate)  # In case that assessor data is not available
        
    return value 


################# Extract city data from county database ###########################
for year in range(2006,2020):
      df = pd.read_csv('Assessor data LA county/LA_property_tax'+str(year)+'.csv')
      LA = df[df['City']=='LOS ANGELES CA']
     
      LA = LA[['AIN','City','ZIPcode5','PropertyLocation','PropertyType',\
                  'PropertyUseCode','GeneralUseType','SpecificUseType',\
                  'YearBuilt','SQFTmain','Bedrooms', 'Bathrooms','Units',\
                  'TotalLandImpValue','CENTER_LAT','CENTER_LON']] 
         
      LA.to_csv('Assessor data LA city/Property_tax'+str(year)+'.csv')


############################## Add building characteristics #########################
df = pd.read_csv('Assessor data LA city/Property_tax2019.csv', index_col=0)
df2 = pd.read_csv('SoftStory_condo_list_clean.csv', index_col=False)
df3 = pd.merge(df, df2, how='right', left_on='AIN', right_on='APN')
df3.dropna(how='any', inplace=True)   # Drop rows with missing data
df3.to_csv('SoftStory_single.csv')


############################### Add assessed value ##################################
for year in range(2006,2019):
    df = pd.read_csv('Assessor data LA city/Property_tax'+str(year)+'.csv', index_col=0)
    value = df[['TotalLandImpValue','AIN']]
    df3 = pd.merge(value, df3, how='right', left_on='AIN', right_on='APN')
    
df3.dropna(how='any', inplace=True)   # Drop rows with missing data
df3.to_csv('SoftStory_single_assessment.csv')

## After modifying column names
df4 = pd.read_csv('SoftStory_single_assessment.csv')

for year in range(2006,2020):
    df4[str(year)] = df4[str(year)].apply(lambda x: float(x.split()[0].replace(',', '')))
    
value2 = convertor2(df4, 2006, 2019)
value2 = pd.concat(value2, axis=1).T   # Convert list of pd series to pd frame
df4 = pd.concat([df4,value2], axis=1)
df4.to_csv('SoftStory_single_assessment.csv')


################################# Add sales data ######################################
df5 = pd.read_csv('')  # Sales data is not available.
df6 = pd.read_csv('SoftStory_single.csv')
df6['APN'] = df6['APN'].astype(str)
df7 = pd.merge(df5, df6, how='right', on='APN')
df7.dropna(how='any', inplace=True)   # Drop rows with missing data


