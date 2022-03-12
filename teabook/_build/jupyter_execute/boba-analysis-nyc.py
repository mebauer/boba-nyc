#!/usr/bin/env python
# coding: utf-8

# # Obsessed with Boba? Analyzing Bubble Tea Shops in NYC Using the Yelp Fusion API
# Exploratory Data Analysis

# In[1]:


import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from PIL import Image

get_ipython().run_line_magic('matplotlib', 'inline')
sns.set(color_codes=True)


# In[2]:


# read in data and preview first five rows
df = pd.read_csv('boba-nyc.csv')

df.head()


# In[3]:


# preview last five rows
df.tail()


# In[4]:


rows, columns = df.shape
print('number of rows: {}\nnumber of columns: {}'.format(rows, columns))


# In[5]:


# review concise summary of data
df.info()


# In[6]:


# identifiying number of nulls and percentage of total per column
ser1 = df.isnull().sum().sort_values(ascending=False)
ser2 = round((df.isnull().sum().sort_values(ascending=False) / len(df)) * 100, 2)

pd.concat([ser1.rename('null_count'), ser2.rename('null_perc')], axis=1)


# In[7]:


# descriptive statistics of numeric columns
df.describe()


# In[8]:


# descriptive statistics of string/object columns
df.describe(include=['O']).T


# In[9]:


# confirm that unique id is actually unique
print('id is unique: {}'.format(df['id'].is_unique))


# In[10]:


df.head()


# In[11]:


# identify number of unique bubble tea shop entries
names_counts = df['name'].value_counts().reset_index()
names_counts = names_counts.rename(columns={'index':'name', 'name':'counts'})

print('number of unique bubble tea shops: {}'.format(len(names_counts)))
names_counts


# In[12]:


# check for duplicates - white spaces, mispellings, etc
lst = []
for row in range(len(names_counts)):
    value = names_counts['name'][row].replace(' ', '').lower()
    lst.append(value)  
    
names_counts = pd.concat([names_counts, pd.Series(lst).rename('name_lower')], axis=1)
names_counts.head()    


# In[13]:


# there are duplicate entries
names_counts['name_lower'].value_counts().head(10)


# In[14]:


# return list of duplicate entries that need to be replaced
duplicates_ser = names_counts['name_lower'].value_counts() > 1
duplicates = duplicates_ser.loc[duplicates_ser].index

duplicates.to_list()


# In[15]:


names_counts = names_counts.loc[names_counts['name_lower'].isin(duplicates.to_list())].sort_values(by='name_lower')

names_counts


# In[16]:


# a dictionary of formatted names (lower & remove white spice) and new names to be returned
new_names = {'yifangtaiwanfruittea':'Yi Fang Taiwan Fruit Tea',
             'vivibubbletea':'Vivi Bubble Tea',
             'jooyteashoppe':'JOOY Tea Shop',
             'tbaar':'TBaar',
             'cocofreshtea&juice':'CoCo Fresh Tea & Juice',
             "yomie'sricexyogurt":"Yomie's Rice X Yogurt",
             'pokébowlstation':'PokéBowl Station'}

names_counts['name_lower'] = names_counts['name_lower'].replace(new_names)

names_counts


# In[17]:


# a dictionary of old and new names to be returned
replace_duplicates = dict(zip(names_counts['name'], names_counts['name_lower']))

replace_duplicates


# In[18]:


# replace old and new names to original dataframe
df['name'] = df['name'].replace(replace_duplicates)

df.head()


# In[19]:


df.to_csv('boba-nyc-cleaned.csv', index=False)


# In[20]:


# count of unique values of bubble tea shops
df['name'].value_counts()


# In[21]:


df['name'].value_counts().reset_index(drop=False)


# In[22]:


names_counts = df['name'].value_counts().reset_index(drop=False)
names_counts = names_counts.rename(columns={'index':'names', 'name':'counts'})

fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(x='counts',
            y="names", 
            data=names_counts.head(10), 
            ax=ax)

plt.title('Number of bubble tea shops by business in nyc', fontsize=15)
plt.tight_layout()


# In[23]:


review_count_df = df.groupby(by='name')['review_count'].mean().sort_values(ascending=False)
review_count_df = round(review_count_df, 2)
review_count_df = review_count_df.reset_index()

review_count_df.head()


# In[24]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(x="review_count", 
            y="name", 
            data=review_count_df.head(20), 
            ax=ax)

plt.title('Average number of reviews per business in nyc', fontsize=15)
plt.tight_layout()


# In[25]:


most_reviewed = df.sort_values(by='review_count', ascending=False).head(20)

most_reviewed.head()


# In[26]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(x="review_count", 
            y="alias", 
            data=most_reviewed, 
            ax=ax)

plt.title('Most reviews per business location in nyc', fontsize=15)
plt.tight_layout()


# In[27]:


df['rating'].describe()


# In[28]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.countplot(data=df, 
             x="rating")

plt.title('Count of ratings per business location in nyc', fontsize=15)
plt.tight_layout()


# In[29]:


price_df = df['price'].dropna().value_counts()
price_df = price_df.reset_index()
price_df.columns = ['price', 'counts']

price_df


# In[30]:


price_df['price'] = price_df['price'].str.count('\\$')

price_df


# In[31]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(y="counts", 
            x="price", 
            data=price_df, 
            ax=ax)

plt.title('Price level (1 = $) per business location in NYC', fontsize=15)
plt.tight_layout()


# In[32]:


url = 'https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=Shapefile'
neighborhoods = gpd.read_file(url)

neighborhoods.head()


# In[33]:


neighborhoods.crs


# In[34]:


neighborhoods = neighborhoods.to_crs('EPSG:4326')

neighborhoods.crs


# In[35]:


df.head()


# In[36]:


gdf = gpd.GeoDataFrame(df, crs=4326,
      geometry=gpd.points_from_xy(df.longitude, df.latitude))

gdf.head()


# In[37]:


join_df = gpd.sjoin(gdf, 
                    neighborhoods, 
                    op='intersects') 

join_df.head()


# In[38]:


join_df = join_df.groupby(by=['ntaname', 'shape_area'])['id'].count().sort_values(ascending=False)
join_df = join_df.reset_index()

join_df = join_df.rename(columns={'id':'counts'})
join_df['counts_squaremile'] = join_df['counts'] / 27878400

join_df.head()


# In[40]:


fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x="counts", 
            y="ntaname", 
            data=join_df.head(20), 
            ax=ax)

plt.title('Most bubble tea locations per neighborhood in NYC', fontsize=15)
plt.ylabel('neighborhood')
plt.xlabel('count per square mile')

plt.tight_layout()
plt.savefig('busineses-per-neighborhood.png', dpi=200)


# In[43]:


fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x="counts_squaremile", 
            y="ntaname", 
            data=join_df.head(20), 
            ax=ax)

plt.title('Most bubble tea locations per neighborhood square mile in NYC', fontsize=15)
plt.ylabel('neighborhood')
plt.xlabel('count per square mile')

plt.tight_layout()
plt.savefig('busineses-per-neighborhood.png', dpi=200)


# In[ ]:




