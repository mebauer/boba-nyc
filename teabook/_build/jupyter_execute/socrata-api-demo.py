#!/usr/bin/env python
# coding: utf-8

# # Intro to the Socrata API with the NYC Dog Licensing Dataset & Python

# In[1]:


# importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sodapy import Socrata
import plotly.express as px
from urllib.request import urlopen
import json
# from IPython.core.display import display, HTML
from IPython.display import IFrame
pd.options.display.max_rows = 100


# ## What is an API?
# 
# The Socrata API follows the REST (REpresentational State Transfer) design pattern.
# 
# REST stands for REpresentational State Transfer. It originally had a more abstract meaning, but has come to be a shorthand name for web sites that act a bit like python functions, taking as inputs values for certain parameters and producing outputs in the form of a long text string.
# 
# API stands for Application Programming Interface. An API specifies how an external program (an application program) can request that a program perform certain computations.
# 
# Putting the two together, a REST API specifies how external programs can make HTTP requests to a web site in order to request that some computation be carried out and data returned as output. When a website is designed to accept requests generated by other computer programs, and produce outputs to be consumed by other programs, it is sometimes called a web service, as opposed to a web site which produces output meant for humans to consume in a web browser.

# ## Anatomy of a URL with the Socrata API
# 
# For this demonstration we will be making requests to the Socrata API with the The [NYC Dog License Dataset](https://data.cityofnewyork.us/Health/NYC-Dog-Licensing-Dataset/nu7n-tubp).
# 
# Components of the url:
# - headers
# - endpoints
# - parameters
# - API key
# 
# In a REST API, the client or application program makes an HTTP request that includes information about what kind of request it is making. Web sites are free to define whatever format they want for how the request should be formatted. 
# 
# In this format, the URL has a standard structure:
# 
# - the base URL: https://data.cityofnewyork.us/resource/nu7n-tubp.json
# - a ? character
# - or more key-value pairs (parameters), formatted as key=value pairs and separated by the & character
# 
# For example, consider the following url requests to the NYC Dog License Dataset with the Socrata API:
# - https://data.cityofnewyork.us/resource/nu7n-tubp.json?rownumber=40895
# - https://data.cityofnewyork.us/resource/nu7n-tubp.json?licenseissueddate=2014-09-12T00:00:00.000
# - https://data.cityofnewyork.us/resource/nu7n-tubp.json?animalname=PAIGE&zipcode=10035
# 
# Try copying that URL into a browser, or just clicking on it. Depending on your browser, it may put the contents into a file attachment that you have to open up to see the contents, or it may just show the contents in a browser window.

# ## API Documentation
# The [API documentation](https://dev.socrata.com/foundry/data.cityofnewyork.us/nu7n-tubp) for the NYC Dog License Dataset contains all of the parts of the url that we need. The fields in the documentation describe the parameters we can use to filter the data in the url request. It is important to read the API documentation for every dataset you use in NYC Open Data, as each dataset has unique features that need to be considered when making requests.

# ## Application Tokens
# 
# [Generating App Tokens and API Keys](https://support.socrata.com/hc/en-us/articles/210138558-Generating-an-App-Token)

# ## Using the Socrata client to make requests
# We are using the Python sodapy library to make our request. The client sends our request for the data, and the API sends the data to us in .json format. Then the pandas library is used to format the results into a dataframe. The Socrata().get() method is used with parameters to filter the data in our request. Check out the [SoSQL examples](https://github.com/xmunoz/sodapy/blob/master/examples/soql_queries.ipynb) in the sodapy github for more info.  The filters use the [SoSQL statements](https://dev.socrata.com/docs/queries/), which are based on SQL and have similar syntax.

# In[2]:


# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cityofnewyork.us", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata('data.cityofnewyork.us',
#                  'appTOKEN',
#                   username='username',
#                   password='password')

# Results returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("nu7n-tubp", 
                     limit=5000,
                     where = "extract_year = '2017' AND breedname = 'Boxer'",
                     select = "animalname, breedname, zipcode, extract_year",
                     order = "zipcode"
                    )

# Convert to pandas DataFrame
doggy_data = pd.DataFrame.from_records(results)
doggy_data['count'] = 1


# In[3]:


doggy_data.info()


# In[4]:


doggy_data.head(20)


# In[5]:


doggy_data['breedname'].unique()


# In[6]:


doggy_data['extract_year'].unique()


# ## Visualize the data with plotly express

# In[7]:


# create grouped dataframe by count of dog registration by zipcode
doggy_zips_grouped = doggy_data[['zipcode', 'count']].groupby(by = 'zipcode').sum().reset_index()

# use GeoJSON file from NYC opendata which contains GIS data for zip code boundaries in NYC
# web page with info on data set url here: 
# https://data.cityofnewyork.us/Health/Modified-Zip-Code-Tabulation-Areas-MODZCTA-/pri4-ifjk
with urlopen('https://data.cityofnewyork.us/resource/pri4-ifjk.geojson') as response:
    zip_codes = json.load(response)


fig = px.choropleth_mapbox(doggy_zips_grouped, geojson=zip_codes, locations='zipcode', color='count',
                           featureidkey='properties.modzcta',
                           color_continuous_scale="Viridis",
                           range_color=(0, max(doggy_zips_grouped['count'])),
                           mapbox_style="carto-positron",
                           zoom=9.25, center = {"lat": 40.743, "lon": -73.988},
                           opacity=0.5,
                           labels={},
                           title="Number of Dog License Registrations in NYC by Zipcode"
                          ).update(layout=dict(title=dict(x=0.5)))
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
fig.show()
# fig.write_html('export/doggy-zip-map.html')
# display(HTML('export/doggy-zip-map.html'))
# IFrame(src = 'export/doggy-zip-map.html', width=700, height=600)


# In[ ]:



