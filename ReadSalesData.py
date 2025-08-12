salesurl='https://raw.githubusercontent.com/Twin-Cities-Data/Datasets/refs/heads/main/Property_Sales_2019_to_2023.csv'
import pandas as pd
dfSales=pd.read_csv(salesurl)
#A little cleaning first before we turn our df into a spark df
dfSales['PIN']=dfSales['PIN'].str.replace('-','')
dfSales=dfSales[['PIN','SALE_DATE','COMMUNITY_DESC','NBHD_DESC','PROPTYPE_DESC','GROSS_SALE_PRICE','DOWNPAYMENT']].\
    dropna(subset='GROSS_SALE_PRICE').\
    fillna(0).\
    query('GROSS_SALE_PRICE>0')
# Turn pandas DF to spark DF
dfSales = spark.createDataFrame(dfSales)

#Grab the parcel data
url='https://raw.githubusercontent.com/Twin-Cities-Data/Datasets/refs/heads/main/Assessing_Department_Parcel_Data_2024_Trim.csv'
df=pd.read_csv(url)
df=df.drop_duplicates(['X','Y']).reset_index()
df['PIN']=df['PIN'].str.replace('p','')
df=spark.createDataFrame(df)
