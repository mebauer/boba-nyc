#!/usr/bin/env python
# coding: utf-8

# # Obsessed with Boba? Analyzing Bubble Tea Shops in NYC Using the Yelp Fusion API
# Data Wrangling: Retrieving Bubble Tea Shops in NYC Using Yelp Fusion API

# In this notebook, we use the Yelp Fusion API to read in data about Bubble Tea Shops in NYC. Additionally, we preview the data, examine the number of rows and columns, and clip only shops that are within NYC's five boroughs. This output data will be the data we use throughout the project.

# # Importing libraries

# In[1]:


# importing libraries
import os
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
# from decouple import AutoConfig


# # Retrieving data from Yelp API

# In[2]:


'''API only returns 1,000 results and 50 per request 
   we use the offset parameter to page through to the next 50 
   source: https://www.yelp.com/developers/faq'''

# saving yelp api key as an environment variable
API_KEY = os.environ.get('yelp_api')
# if API_KEY is None:
#     config = AutoConfig(search_path = '.')
#     API_KEY = config('YELP_API')

# empty list to place our data for each page
lst = []

# our offset parameter - each page 50 rows
offset = 0
print('initial offset number: {}'.format(offset))

# loop through the api 20 times (limit is 1000 rows with each page includes 50 rows)
for i in range(20):
    
    try:
        headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
        search_api_url = 'https://api.yelp.com/v3/businesses/search'
        params = {'term': 'bubble tea', 
                  'categories': 'bubbletea, boba',
                  'location': 'New York City',
                  'offset': offset,
                  'limit': 50}

        response = requests.get(search_api_url, 
                                headers=headers, 
                                params=params, 
                                timeout=10)

        # return a dictionary
        data_dict = response.json()
        
        # convert the business dictionary to a pandas dataframe and append to list
        data = pd.DataFrame(data_dict['businesses'])
        lst.append(data)
      
        # add 50 to the offset to access a new page
        offset += 50
        print('current offset number: {}'.format(offset))
        
    except Exception as ex:
        print('exception: {}\nexit loop.'.format(ex))
        break

# concatenate all pages to one dataframe and reset index
df = pd.concat(lst)
df = df.reset_index(drop=True)

# review shape of dataframe
rows, columns = df.shape
print()
print('query includes {:,} rows and {} columns.'.format(rows, columns))
print('row id is unique: {}.'.format(df['id'].is_unique))

# review if dataframe id is unique, if not drop duplicates
if df['id'].is_unique == False:
    duplicates = df.loc[df.duplicated(subset=['id'])]
    vals = list(duplicates.head()['name'].values)
    print('\nduplicates found: {}.'.format(vals))
    
    df = df.drop_duplicates(subset=['id']).reset_index(drop=True)
    print('dropping duplicates...')
    
    rows, columns = df.shape
    print('\nrow id is unique: {}.'.format(df['id'].is_unique))
    print('query includes {:,} rows and {} columns.'.format(rows, columns))


# # Inspect data

# In[117]:


# preview first five rows
df.head()


# In[118]:


# preview last five rows
df.tail()


# In[119]:


# preview column datatypes and non-null counts
df.info()


# In[120]:


# return count of unique values of bubble tea shops
df['name'].value_counts()


# In[121]:


# return top 20 count of unique values of bubble tea shops
df['name'].value_counts().head(20)


# # Inspect categories

# In[122]:


df['categories'].head()


# In[123]:


df['categories'].apply(pd.Series)


# In[124]:


categories_df = df['categories'].apply(pd.Series)
categories_df.columns = ['cat_1', 'cat_2', 'cat_3']

categories_df


# # Check for duplicates

# In[125]:


# identify number of unique bubble tea shop entries
names_counts = df['name'].value_counts().reset_index()
names_counts = names_counts.rename(columns={'index':'name', 'name':'counts'})

print('number of unique bubble tea shops: {}'.format(len(names_counts)))
names_counts


# In[126]:


# check for duplicates - white spaces, mispellings, etc
lst = []
for row in range(len(names_counts)):
    value = names_counts['name'][row].replace(' ', '').lower()
    lst.append(value)  
    
names_counts = pd.concat([names_counts, pd.Series(lst).rename('name_lower')], axis=1)
names_counts.head()    


# In[127]:


# there are duplicate entries
names_counts['name_lower'].value_counts().head(10)


# In[128]:


# return list of duplicate entries that need to be replaced
duplicates_ser = names_counts['name_lower'].value_counts() > 1
duplicates = duplicates_ser.loc[duplicates_ser].index

print('these places have dulicate entries:\n')
for dup in duplicates.to_list():
    print(dup)  


# In[129]:


names_counts = (names_counts.loc[names_counts['name_lower'].isin(duplicates.to_list())]
                .sort_values(by='name_lower'))

names_counts


# In[130]:


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


# In[131]:


# a dictionary of old and new names to be returned
replace_duplicates = dict(zip(names_counts['name'], names_counts['name_lower']))

replace_duplicates


# In[132]:


# replace old and new names to original dataframe
df['name'] = df['name'].replace(replace_duplicates)

df.head()


# In[133]:


df['name'].value_counts().head(20)


# # Clip shops within NYC

# In[134]:


# explode coordinates to create an individual column
gdf = pd.concat([df, df['coordinates'].apply(pd.Series)], axis=1)

# retrieve lat, lon values and return a geodataframe
gdf = gpd.GeoDataFrame(gdf, crs=4326, 
      geometry=gpd.points_from_xy(gdf.longitude, gdf.latitude))

gdf.head()


# In[135]:


# read in boroughs shapefile to return only bubble tea shops within nyc
url = 'https://data.cityofnewyork.us/api/geospatial/tqmj-j8zm?method=export&format=Shapefile'
boro_gdf = gpd.read_file(url)

boro_gdf.head()


# In[136]:


# plot bubble tea shops and boroughs
fig, ax = plt.subplots(figsize=(8, 8))

gdf.plot(ax=ax)
boro_gdf.plot(ax=ax, facecolor='None', edgecolor='black', zorder=0)

plt.title('bubble tea shops in NYC area')
plt.xlabel('lon')
plt.ylabel('lat')
plt.tight_layout()


# In[137]:


# clip bubble tea shops that are within the five boroughs
gdf = gpd.clip(gdf, boro_gdf)
gdf = gdf.reset_index(drop=True)

rows, columns = gdf.shape
print('number of rows: {}\nnumber of columns: {}'.format(rows, columns))


# In[138]:


# preview dataframe
gdf.head()


# In[139]:


fig, ax = plt.subplots(figsize=(8, 8))

gdf.plot(ax=ax)
boro_gdf.plot(ax=ax, facecolor='None', edgecolor='black', zorder=0)

plt.title('bubble tea shops in NYC')
plt.xlabel('lon')
plt.ylabel('lat')
plt.tight_layout()


# In[140]:


# # save file
# gdf.to_csv('boba-nyc.csv', index=False)


# In[141]:


# # sanity check
# pd.read_csv('boba-nyc.csv').head()


# In[ ]:




