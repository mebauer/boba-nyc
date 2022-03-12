#!/usr/bin/env python
# coding: utf-8

# ## Maps

# In[1]:


import os
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
# import seaborn as sns
import requests
from PIL import Image

# %matplotlib inline
# sns.set(color_codes=True)


# In[2]:


df = pd.read_csv('boba-nyc.csv')
df.head()


# In[3]:


df.describe()


# In[4]:


df.describe(include=['O']).T


# In[5]:


url = 'https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=Shapefile'
neighborhoods = gpd.read_file(url)
neighborhoods.head()


# In[6]:


neighborhoods.to_crs(epsg=4326)
gdf = gpd.GeoDataFrame(df, crs=neighborhoods.crs, geometry=gpd.points_from_xy(df.longitude, df.latitude))
print(neighborhoods.crs)
print(gdf.crs)


# In[8]:


join_df = gpd.sjoin(gdf, neighborhoods, how="left")
print(join_df.shape)
join_df.head()


# In[10]:


group_nt = join_df.groupby(by='ntaname')['id'].count().sort_values(ascending=True)
group_nt = group_nt.reset_index()
group_nt.columns = ['ntaname', 'counts']
group_nt.head()
group_nt.describe()


# In[11]:


group_nt.loc[group_nt.counts==0, 'cnt_category'] = 0
group_nt.loc[group_nt.counts>0, 'cnt_category'] = 1
group_nt.loc[group_nt.counts>4, 'cnt_category'] = 3
group_nt.loc[group_nt.counts>10, 'cnt_category'] = 4
group_nt.astype({'cnt_category':int})


# In[12]:


nt_rating = join_df.groupby(by='ntaname')['rating'].mean().sort_values(ascending=True)
nt_rating = nt_rating.reset_index()
nt_rating.columns = ['ntaname','rating']
nt_rating.describe()
# nt_rating.head()


# In[13]:


group_nt = group_nt.merge(nt_rating, how="left", left_on='ntaname', right_on='ntaname')
group_nt.head()


# In[14]:


group_nt_gdf = neighborhoods.merge(group_nt, how='left', left_on='ntaname', right_on='ntaname')
# group_nt_gdf['counts'].fillna(0, inplace=True)
# group_nt_gdf['cnt_category'].fillna(0, inplace=True)
group_nt_gdf.describe()


# In[15]:


group_nt_gdf['label_geometry'] = group_nt_gdf['geometry'].centroid
group_nt_gdf.sort_values('counts', ascending=True)
group_nt_gdf.head()


# In[19]:


fig, ax = plt.subplots(figsize=(20, 12), sharey=False)
# neighborhoods.plot(ax=ax, edgecolor="grey", linewidth=0.4, facecolor='none')
missing_kwds={"color": "lightgrey","edgecolor": "lightgrey","label": "Missing values"}
group_nt_gdf.plot(ax=ax, column='counts', colormap='OrRd', edgecolor="none", linewidth=1, legend=True, legend_kwds = {'label': "Counts of Boba Tea Shops in NYC Neighborhoods"}, missing_kwds=missing_kwds)

top_counts = group_nt_gdf.sort_values("counts", ascending=False)[0:3]
for x, y, label in zip(top_counts.label_geometry.x, top_counts.label_geometry.y, top_counts.ntaname):
    ax.annotate(label, xy=(x, y))

ax.set_axis_off()


# In[20]:


fig, ax = plt.subplots(figsize=(20, 12), sharey=False)

missing_kwds={"color": "lightgrey","edgecolor": "lightgrey","label": "Missing values"}
group_nt_gdf.plot(
    ax=ax, column='rating', colormap='BuPu', edgecolor="none", linewidth=1, legend=True,
    legend_kwds = {'label': "Rating of Boba Tea Shops in NYC Neighborhoods"}, missing_kwds=missing_kwds)

top_rated = group_nt_gdf.sort_values("rating", ascending=False)[0:3]
for x, y, label in zip(top_rated.label_geometry.x, top_rated.label_geometry.y, top_rated.ntaname):
    ax.annotate(label, xy=(x, y))
ax.set_axis_off()


# In[69]:


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
    ax=ax[1], column='rating', colormap='BuPu', edgecolor="none", linewidth=1, legend=True, missing_kwds=missing_kwds)

ax[0].set_axis_off()
ax[1].set_axis_off()


# In[55]:


list(group_nt_gdf_pt.loc[(group_nt_gdf_pt.counts).isna()]['ntaname']) ==  list((group_nt_gdf_pt.loc[(group_nt_gdf_pt.rating).isna()])['ntaname'])
group_nt_gdf_pt.loc[group_nt_gdf_pt.ntaname=='Battery Park City-Lower Manhattan']


# group_nt_gdf_pt.plot(ax=ax[1], colormap='BuPu', column="rating", markersize=np.power(group_nt_gdf_pt.rating,2) * 20, alpha=0.5, edgecolor='#2e2622', linewidth=0.4, legend=True, missing_kwds=missing_kwds)
group_nt_gdf_pt.plot(ax=ax[1], colormap='BuPu', column="rating", markersize=group_nt_gdf_pt.counts * 80, alpha=0.9, edgecolor='#2e2622', linewidth=0.4, legend=True)


# In[ ]:




