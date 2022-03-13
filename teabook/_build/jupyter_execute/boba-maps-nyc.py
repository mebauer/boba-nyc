#!/usr/bin/env python
# coding: utf-8

# # Boba Maps of NYC

# In[1]:


import os
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
from PIL import Image


# In[2]:


df = pd.read_csv('boba-nyc.csv')
df.head()


# In[3]:


df.describe()


# In[4]:


df.describe(include=['O']).T


# ### Map Boba data for NYC neighborhoods

# In[5]:


# read neighborhood data as geodataframe
url = 'https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=Shapefile'
neighborhoods = gpd.read_file(url)
neighborhoods.head()


# In[6]:


# re-project neighborhood data
neighborhoods.to_crs(epsg=4326)

# open the boba dataframe as geo data frame using the lat-long info in the data
gdf = gpd.GeoDataFrame(df, crs=neighborhoods.crs, geometry=gpd.points_from_xy(df.longitude, df.latitude))

print(neighborhoods.crs)
print(gdf.crs)


# In[7]:


# join the neighborhood information to each boba shop
join_df = gpd.sjoin(gdf, neighborhoods, how="left")
print(join_df.shape)
join_df.head()


# In[8]:


# get the counts of boba shops groupped by neighborhood names

group_nt = join_df.groupby(by='ntaname')['id'].count().sort_values(ascending=True)
group_nt = group_nt.reset_index()
group_nt.columns = ['ntaname', 'counts']
group_nt.head()
group_nt.describe()


# In[9]:


# get the average ratings of boba shops groupped by neighborhood names

nt_rating = join_df.groupby(by='ntaname')['rating'].mean().sort_values(ascending=True)
nt_rating = nt_rating.reset_index()
nt_rating.columns = ['ntaname','rating']
nt_rating.describe()
# nt_rating.head()


# In[10]:


# merge the counts by neighborhood dataframe and ratings by neighborhood dataframe
group_nt = group_nt.merge(nt_rating, how="left", left_on='ntaname', right_on='ntaname')
group_nt.head()


# In[11]:


# merge the counts and ratings by neighborhood dataframe with the neighborhood geodataframe to get the spatial information
group_nt_gdf = neighborhoods.merge(group_nt, how='left', left_on='ntaname', right_on='ntaname')
group_nt_gdf.describe()


# In[12]:


# get the lat-long of the centroid of each neighborhood ("label_geometry") for labeling
group_nt_gdf['label_geometry'] = group_nt_gdf['geometry'].centroid
group_nt_gdf.sort_values('counts', ascending=True)
group_nt_gdf.head()


# In[13]:


# create a choropleth map of boba shop counts in NYC neighborhoods

fig, ax = plt.subplots(figsize=(20, 12), sharey=False)
missing_kwds={"color": "lightgrey","edgecolor": "lightgrey","label": "Missing values"}
group_nt_gdf.plot(ax=ax, column='counts', cmap='OrRd', edgecolor="none", linewidth=1, legend=True, legend_kwds = {'label': "Counts of Boba Tea Shops in NYC Neighborhoods"}, missing_kwds=missing_kwds)

top_counts = group_nt_gdf.sort_values("counts", ascending=False)[0:3]
for x, y, label in zip(top_counts.label_geometry.x, top_counts.label_geometry.y, top_counts.ntaname):
    ax.annotate(label, xy=(x, y))

ax.set_axis_off()


# In[14]:


# create a choropleth map of average boba shop ratings in NYC neighborhoods

fig, ax = plt.subplots(figsize=(20, 12), sharey=False)

missing_kwds={"color": "lightgrey","edgecolor": "lightgrey","label": "Missing values"}
group_nt_gdf.plot(
    ax=ax, column='rating', cmap='BuPu', edgecolor="none", linewidth=1, legend=True,
    legend_kwds = {'label': "Rating of Boba Tea Shops in NYC Neighborhoods"}, missing_kwds=missing_kwds)

top_rated = group_nt_gdf.sort_values("rating", ascending=False)[0:3]
for x, y, label in zip(top_rated.label_geometry.x, top_rated.label_geometry.y, top_rated.ntaname):
    ax.annotate(label, xy=(x, y))
ax.set_axis_off()


# In[15]:


# create a choropleth map of boba shop ratings in NYC neighborhoods
# and a proportional symbol map of boba shop counts in NYC neighborhoods

fig, ax = plt.subplots(1,2, figsize=(20, 12), sharey=False)


# draw counts of boba tea shops
group_nt_gdf_pt = group_nt_gdf.copy()
group_nt_gdf_pt['geometry'] = group_nt_gdf_pt['label_geometry']
group_nt_gdf_pt.head()

ax[0].title.set_text('Counts of Boba Shops in NYC')
neighborhoods.plot(ax=ax[0], color="#ebd7b8", edgecolor="white",linewidth=0.5, alpha=1) #gainsboro
group_nt_gdf_pt.plot(ax=ax[0], color="#2e2622", markersize=group_nt_gdf_pt.counts * 50, alpha=0.5, edgecolor='#2e2622', linewidth=0.4, legend=True, legend_kwds = {'label': "Counts of Boba Tea Shops in NYC Neighborhoods"})


# draw average rating of boba tea shops
ax[1].title.set_text('Average Ratings of Boba Shops in NYC')
missing_kwds={"color": "lightgrey","edgecolor": "lightgrey","label": "Missing values"}
group_nt_gdf.plot(
    ax=ax[1], column='rating', cmap='BuPu', edgecolor="none", linewidth=1, legend=True, missing_kwds=missing_kwds)

ax[0].set_axis_off()
ax[1].set_axis_off()

