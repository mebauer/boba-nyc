#!/usr/bin/env python
# coding: utf-8

# # Boba Maps of NYC
# ### Best NYC Neighborhoods for Boba Lovers?

# In[1]:


### Imports for Google Colab Session

# # imports for Google Colab Sessions
# !apt install gdal-bin python-gdal python3-gdal 
# # Install rtree - Geopandas requirment
# !apt install python3-rtree 
# # Install Geopandas
# !pip install git+git://github.com/geopandas/geopandas.git
# # Install descartes - Geopandas requirment
# !pip install descartes 


# In[2]:


import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# In[3]:


url = 'https://raw.githubusercontent.com/mebauer/boba-nyc/master/teabook/boba-nyc.csv'
df = pd.read_csv(url)
df.head()


# In[4]:


df.describe()


# In[5]:


df.describe(include=['O']).T


# ## Map Boba Data for NYC Neighborhoods

# In[6]:


# read neighborhood data as geodataframe
url = 'https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=Shapefile'
neighborhoods = gpd.read_file(url)
neighborhoods.head()


# In[7]:


# re-project neighborhood data
neighborhoods = neighborhoods.to_crs('EPSG:4326')

# open the boba dataframe as geo data frame using the lat-long info in the data
gdf = gpd.GeoDataFrame(df, crs=neighborhoods.crs, geometry=gpd.points_from_xy(df.longitude, df.latitude))

print(neighborhoods.crs)
print(gdf.crs)


# In[10]:


# join the neighborhood information to each boba shop
join_df = gpd.sjoin(gdf, neighborhoods, how="left")
print(join_df.shape)
join_df.head()


# In[11]:


# get the counts of boba shops groupped by neighborhood names
nt_count = join_df.groupby(by='ntaname')['id'].count().sort_values(ascending=True)
nt_count = nt_count.reset_index()
nt_count.columns = ['ntaname', 'counts']
nt_count.describe()


# In[12]:


# get the average ratings of boba shops groupped by neighborhood names
nt_rating = join_df.groupby(by='ntaname')['rating'].mean().sort_values(ascending=True)
nt_rating = nt_rating.reset_index()
nt_rating.columns = ['ntaname','rating']
nt_rating.describe()


# In[13]:


# get the average ratings of boba shops groupped by neighborhood names
nt_revcount = join_df.groupby(by='ntaname')['review_count'].sum().sort_values(ascending=True)
nt_revcount = nt_revcount.reset_index()
nt_revcount.columns = ['ntaname','review_count']
nt_revcount.describe()


# In[14]:


# merge the counts, ratings, review counts by neighborhood dataframe to the neighborhood geodataframe, which contains spatial information of the neighborhoods
group_nt_gdf = neighborhoods.merge(nt_count, how="left", left_on='ntaname', right_on='ntaname')
group_nt_gdf = group_nt_gdf.merge(nt_rating, how="left", left_on='ntaname', right_on='ntaname')
group_nt_gdf = group_nt_gdf.merge(nt_revcount, how="left", left_on='ntaname', right_on='ntaname')

group_nt_gdf.head()


# In[15]:


# get the lat-long of the centroid of each neighborhood ("label_geometry") for labeling
group_nt_gdf['label_geometry'] = group_nt_gdf['geometry'].centroid
group_nt_gdf.sort_values('counts', ascending=True)
group_nt_gdf.head()


# In[16]:


# create a choropleth map of boba shop counts in NYC neighborhoods

fig, ax = plt.subplots(figsize=(20, 12))
missing_kwds={"color": "lightgrey","edgecolor": "lightgrey","label": "Missing values"}
group_nt_gdf.plot(ax=ax, column='counts', cmap='OrRd', edgecolor="none", linewidth=1, legend=True, legend_kwds = {'label': "Counts of Boba Tea Shops in NYC Neighborhoods"}, missing_kwds=missing_kwds)

# lebel the top 3 neighborhoods
top_counts = group_nt_gdf.sort_values("counts", ascending=False)[0:3]
for x, y, label in zip(top_counts.label_geometry.x, top_counts.label_geometry.y, top_counts.ntaname):
    ax.annotate(label, xy=(x, y))

ax.set_axis_off()


# In[17]:


# create a choropleth map of average boba shop ratings in NYC neighborhoods

fig, ax = plt.subplots(figsize=(20, 12))
missing_kwds={"color": "lightgrey","edgecolor": "lightgrey","label": "Missing values"}
group_nt_gdf.plot(
    ax=ax, column='rating', cmap='BuPu', edgecolor="none", linewidth=1, legend=True,
    legend_kwds = {'label': "Rating of Boba Tea Shops in NYC Neighborhoods"}, missing_kwds=missing_kwds)

# lebel the top 3 neighborhoods
top_rated = group_nt_gdf.sort_values("rating", ascending=False)[0:3]
for x, y, label in zip(top_rated.label_geometry.x, top_rated.label_geometry.y, top_rated.ntaname):
    ax.annotate(label, xy=(x, y))
ax.set_axis_off()


# In[19]:


# Put the maps side to side..
# create a choropleth map of boba shop ratings in NYC neighborhoods
# and proportional symbol maps of boba shop counts and boba shop review counts in NYC neighborhoods

fig, ax = plt.subplots(2, 2, figsize=(30, 25))


# draw average rating of boba tea shops
ax[0][0].title.set_text('Average Ratings of Boba Shops in NYC')
missing_kwds={"color": "lightgrey","edgecolor": "lightgrey","label": "Missing values"}
group_nt_gdf.plot(ax=ax[0][0], 
    column='rating',
    cmap='BuPu',
    edgecolor="none", 
    linewidth=1,
    legend=True,
    legend_kwds = {
        'label': "Rating of Boba Tea Shops in NYC Neighborhoods"
    }, 
    missing_kwds = missing_kwds
)

# To create proportional symbol maps,
# create a copy of the geodataframe using the centroids coordinate as the geometry
group_nt_gdf_pt = group_nt_gdf.copy()
group_nt_gdf_pt['geometry'] = group_nt_gdf_pt['label_geometry']
group_nt_gdf_pt.head()


# draw counts of boba tea shops
ax[0][1].title.set_text('Counts of Boba Shops in NYC')
neighborhoods.plot(ax=ax[0][1], color="#ebd7b8", edgecolor="white",linewidth=0.5, alpha=1)
group_nt_gdf_pt.plot(
    ax=ax[0][1], color="#2e2622", markersize=group_nt_gdf_pt.counts * 50, alpha=0.5, edgecolor='#2e2622', linewidth=0.4, legend=True, label="Counts of Boba Tea Shops in NYC Neighborhoods")


# draw counts of reviews
ax[1][0].title.set_text('Counts of Boba Shops Reviews in NYC')
neighborhoods.plot(ax=ax[1][0], color="#b8bd88", edgecolor="whitesmoke",linewidth=0.5, alpha=1)
group_nt_gdf_pt.plot(
    ax=ax[1][0], color="#2e2622", markersize=group_nt_gdf_pt.review_count / 2, alpha=0.4, edgecolor='#2e2622', linewidth=0.4, legend=True, label="Counts of Boba Shops Reviews in NYC Neighborhoods")

ax[0][0].set_axis_off()
ax[0][1].set_axis_off()
ax[1][0].set_axis_off()
ax[1][1].set_axis_off()

ax[0][1].legend(loc='lower right', markerscale=0.7, frameon=False)
ax[1][0].legend(loc='lower right', markerscale=0.7, frameon=False)


# ### The top-rated neighborhoods seem to have low counts of boba shops and count of reviews.
# 
# - fewer boba shops...less competition?
# - fewer counts of review...less representative rating?

# In[18]:


group_nt_gdf[['rating', 'counts', 'review_count']].describe()


# In[19]:


group_nt_gdf.sort_values("rating", ascending=False).dropna()[0:10]


# ## NYC Neighborhood Boba Index
# 
# ### that take into account counts of reviews and counts of boba shops in the neighborhood?

# In[20]:


# make a copy of the boba dataframe
join_df2 = join_df.copy()


# In[21]:


# make a copy of the neighborhoods geodataframe 
group_nt_gdf2 = group_nt_gdf[['boro_name', 'ntaname', 'geometry', 'label_geometry']].copy()
group_nt_gdf2.head()


# In[22]:


join_df2['rate_rev'] = join_df2['rating'] * join_df2['review_count']
join_df2.head()


# In[23]:


# sum up the (rating * review_count) by neighborhood
nt_raterev2 = join_df2.groupby(by='ntaname')['rate_rev'].sum().sort_values(ascending=True)
nt_raterev2 = nt_raterev2.reset_index()
nt_raterev2.columns = ['ntaname','rate_rev']
nt_raterev2.head()


# In[24]:


# merge to the neighborhood geodataframe
group_nt_gdf2 = group_nt_gdf2.merge(nt_count, how='left', left_on='ntaname', right_on='ntaname')
group_nt_gdf2 = group_nt_gdf2.merge(nt_rating, how='left', left_on='ntaname', right_on='ntaname')
group_nt_gdf2 = group_nt_gdf2.merge(nt_revcount, how='left', left_on='ntaname', right_on='ntaname')

group_nt_gdf2 = group_nt_gdf2.merge(nt_raterev2, how='left', left_on='ntaname', right_on='ntaname')

group_nt_gdf2.head()


# ### The Creation of Boba Index...

# In[25]:


group_nt_gdf2['boba_index'] = (

    # review counts-weighted rating...
    group_nt_gdf2['rate_rev']                        # sum of (rating * review counts) in neighborhood
    / group_nt_gdf2['review_count']                  # / (the total review counts in neighborhood)

    # consider competition...
    * np.sqrt(group_nt_gdf2['counts'])               # * (square root of total boba shop count in neighborhood)
    / (np.sqrt(group_nt_gdf2['counts'])).mean()      # / (mean of square root boba shop count in whole NYC)

)

group_nt_gdf2.head()


# In[26]:


# create a choropleth map of Baba Index in NYC neighborhoods

fig, ax = plt.subplots(figsize=(20, 12), sharey=False)

ax.title.set_text('Boba Index of NYC Neighborhoods')
missing_kwds={"color": "lightgrey","edgecolor": "lightgrey","label": "Missing values"}
group_nt_gdf2.plot(
    ax=ax, column='boba_index', cmap='BuPu', edgecolor="none", linewidth=1, legend=True,
    legend_kwds = {'label': "Boba Index"}, missing_kwds=missing_kwds)

top_rated = group_nt_gdf2.sort_values("boba_index", ascending=False)[0:3]
for x, y, label in zip(top_rated.label_geometry.x, top_rated.label_geometry.y, top_rated.ntaname):
    ax.annotate(label, xy=(x, y))

ax.set_axis_off()


# In[27]:


group_nt_gdf2.sort_values("boba_index", ascending=False).dropna()[0:10]


# In[28]:


group_nt_gdf2.describe()


# In[ ]:




