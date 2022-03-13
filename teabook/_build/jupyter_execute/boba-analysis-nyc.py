#!/usr/bin/env python
# coding: utf-8

# # Obsessed with Boba? Analyzing Bubble Tea Shops in NYC Using the Yelp Fusion API
# Exploratory Data Analysis

# In[1]:


# # imports for Google Colab Sessions
# !apt install gdal-bin python-gdal python3-gdal 
# # Install rtree - Geopandas requirment
# !apt install python3-rtree 
# # Install Geopandas
# !pip install git+git://github.com/geopandas/geopandas.git
# # Install descartes - Geopandas requirment
# !pip install descartes 

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')
sns.set(color_codes=True)


# In[2]:


# google colab path to data
url = 'https://raw.githubusercontent.com/mebauer/boba-nyc/master/teabook/boba-nyc.csv'
df = pd.read_csv(url)

# # local path to data
# df = pd.read_csv('boba-nyc.csv')
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


df['name'].value_counts().reset_index(drop=False)


# In[13]:


names_counts = df['name'].value_counts().reset_index(drop=False)
names_counts = names_counts.rename(columns={'index':'names', 'name':'counts'})

fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(x='counts',
            y="names", 
            data=names_counts.head(10), 
            ax=ax)

plt.title('Number of bubble tea shops by business in nyc', fontsize=15)
plt.tight_layout()


# In[14]:


review_count_df = df.groupby(by='name')['review_count'].mean().sort_values(ascending=False)
review_count_df = round(review_count_df, 2)
review_count_df = review_count_df.reset_index()

review_count_df.head()


# In[15]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(x="review_count", 
            y="name", 
            data=review_count_df.head(20), 
            ax=ax)

plt.title('Average number of reviews per business in nyc', fontsize=15)
plt.tight_layout()


# In[16]:


most_reviewed = df.sort_values(by='review_count', ascending=False).head(20)

most_reviewed.head()


# In[17]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(x="review_count", 
            y="alias", 
            data=most_reviewed, 
            ax=ax)

plt.title('Most reviews per business location in nyc', fontsize=15)
plt.tight_layout()


# In[18]:


df['rating'].describe()


# In[19]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.countplot(data=df, 
             x="rating")

plt.title('Count of Yelp ratings per business location in nyc', fontsize=15)
plt.tight_layout()


# In[20]:


price_df = df['price'].dropna().value_counts()
price_df = price_df.reset_index()
price_df.columns = ['price', 'counts']

price_df


# In[21]:


price_df['price'] = price_df['price'].str.count('\\$')

price_df


# In[22]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(y="counts", 
            x="price", 
            data=price_df, 
            ax=ax)

plt.title('Yelp price level (1 = $) per business location in NYC', fontsize=15)
plt.tight_layout()


# In[23]:


url = 'https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=Shapefile'
neighborhoods = gpd.read_file(url)

neighborhoods.head()


# In[24]:


neighborhoods.crs


# In[25]:


neighborhoods = neighborhoods.to_crs('EPSG:4326')

neighborhoods.crs


# In[26]:


df.head()


# In[27]:


gdf = gpd.GeoDataFrame(df, crs=4326,
      geometry=gpd.points_from_xy(df.longitude, df.latitude))

gdf.head()


# In[28]:


join_df = gpd.sjoin(gdf, 
                    neighborhoods, 
                    op='intersects') 

join_df.head()


# In[29]:


join_df = join_df.groupby(by=['ntaname', 'shape_area'])['id'].count().sort_values(ascending=False)
join_df = join_df.reset_index()

join_df = join_df.rename(columns={'id':'counts'})
join_df['counts_squaremile'] = join_df['counts'] / (join_df['shape_area'] / 27878400)

join_df.head()


# In[30]:


fig, ax = plt.subplots(figsize=(10, 6))
data = join_df.sort_values(by='counts', ascending=False).head(20)

sns.barplot(x="counts", 
            y="ntaname", 
            data=data, 
            ax=ax)

plt.title('Most bubble tea locations per neighborhood in NYC', fontsize=15)
plt.ylabel('neighborhood')
plt.xlabel('count')

plt.tight_layout()
plt.savefig('busineses-per-neighborhood.png', dpi=200)


# In[31]:


fig, ax = plt.subplots(figsize=(10, 6))
data = join_df.sort_values(by='counts_squaremile', ascending=False).head(20)

sns.barplot(x="counts_squaremile", 
            y="ntaname", 
            data=data, 
            ax=ax)

plt.suptitle('Most bubble tea locations per square mile by neighborhood in NYC', 
             fontsize=15,
             y=.96, x=.60)
plt.ylabel('neighborhood')
plt.xlabel('count per square mile')

plt.tight_layout()
plt.savefig('busineses-per-neighborhood.png', dpi=200)


# In[ ]:




