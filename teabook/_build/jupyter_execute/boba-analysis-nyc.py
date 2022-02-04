#!/usr/bin/env python
# coding: utf-8

# # Searching for Boba: Analyzing Bubble Tea Shops in NYC Using the Yelp Fusion API
# 
# Mark Bauer

# In[1]:


import os
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


df = pd.read_csv('boba-nyc.csv')

df.head()


# In[3]:


df.tail()


# In[4]:


rows, columns = df.shape
print('number of rows: {}\nnumber of columns: {}'.format(rows, columns))


# In[5]:


df.info()


# In[6]:


df.isnull().sum().sort_values(ascending=False)


# In[7]:


df.describe()


# In[8]:


df.describe(include=['O']).T


# In[9]:


print('id is unique: {}'.format(df['id'].is_unique))


# In[10]:


df.head()


# In[11]:


names = df['name'].value_counts().reset_index()
names.columns = ['name', 'counts']

names.head()


# In[12]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(x="counts", 
            y="name", 
            data=names.head(20), 
            ax=ax)

plt.title('number of bubble tea shops by business in nyc', fontsize=15)
plt.tight_layout()


# In[13]:


review_count_df = df.groupby(by='name')['review_count'].mean().sort_values(ascending=False)
review_count_df = round(review_count_df, 2)
review_count_df = review_count_df.reset_index()

review_count_df.head()


# In[14]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(x="review_count", 
            y="name", 
            data=review_count_df.head(20), 
            ax=ax)

plt.title('average number of reviews per business in nyc', fontsize=15)
plt.tight_layout()


# In[15]:


most_reviewed = df.sort_values(by='review_count', ascending=False).head(20)

most_reviewed.head()


# In[16]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(x="review_count", 
            y="alias", 
            data=most_reviewed, 
            ax=ax)

plt.title('most reviews per business location in nyc', fontsize=15)
plt.tight_layout()


# In[17]:


df['rating'].describe()


# In[18]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.histplot(data=df, 
             x="rating")

plt.title('distribution of ratings per business location in nyc', fontsize=15)
plt.tight_layout()


# In[19]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.scatterplot(data=df, 
                x="review_count", 
                y="rating", 
                ax=ax)

plt.title('rating vs. review count per business location in nyc', fontsize=15)
plt.tight_layout()


# In[20]:


price_df = df['price'].dropna().value_counts()
price_df = price_df.reset_index()
price_df.columns = ['price', 'counts']

price_df.head()


# In[21]:


price_df['price'] = price_df['price'].str.count('\\$')

price_df


# In[22]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(y="counts", 
            x="price", 
            data=price_df, 
            ax=ax)

plt.title('price level (1 = $) per business location in nyc', fontsize=15)
plt.tight_layout()


# In[23]:


url = 'https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=Shapefile'
neighborhoods = gpd.read_file(url)

neighborhoods.head()


# In[24]:


neighborhoods.crs


# Transform CRS coordinates to avoid the following warning during spatial join:  
# `UserWarning: CRS mismatch between the CRS of left geometries and the CRS of right geometries.`
# 
# _References_:
# 
# [Finding distance of consecutive points in a GeoPandas data frame](https://gis.stackexchange.com/questions/347732/finding-distance-of-consecutive-points-in-a-geopandas-data-frame)
# 
# [geopandas.GeoDataFrame.to_crs](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_crs.html)

# In[25]:


neighborhoods.to_crs('EPSG:4326', inplace = True)


# In[26]:


neighborhoods.crs


# In[27]:


df.head()


# In[28]:


gdf = gpd.GeoDataFrame(df, crs=4326,
      geometry=gpd.points_from_xy(df.longitude, df.latitude))

gdf.head()


# In[29]:


join_df = gpd.sjoin(gdf, 
                    neighborhoods, 
                    predicate='intersects') 

join_df.head()


# In[30]:


join_df = join_df.groupby(by='ntaname')['id'].count().sort_values(ascending=False)
join_df = join_df.reset_index()

join_df.columns = ['nta_name', 'counts']

join_df.head()


# In[31]:


fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x="counts", 
            y="nta_name", 
            data=join_df.head(20), 
            ax=ax)

plt.title('most bubble tea locations per neighborhood in nyc', fontsize=15)
plt.ylabel('neighborhood')
plt.xlabel('count')

plt.tight_layout()
plt.savefig('busineses-per-neighborhood.png', dpi=200)

