# Import Libraries

## External Libraries
import pandas as pd
import streamlit as st
import os
from PIL import Image
import plotly.express as px
import plotly.figure_factory as ff

## Internal Libraries
### None

# Variables
file_path = os.path.dirname(__file__)
file_name = '/img/bubble-tea-cover-img.jpg'
cover_image = Image.open(file_path + file_name)

# Title
## Display Image
st.image(cover_image, use_column_width = True)
st.write(
    """
    # Bubble Tea Shop App

    Analyzing Bubble Tea Shops in NYC
    """
)
with st.expander('Show Info'):
    st.write(
        """
        * **Data Team**: Mark Bauer, Chidi Ezeolu, Ho Hsieh, Nathan Williamson
        * **GitHub**: https://github.com/mebauer/boba-nyc
        * **Jupyter Book**: https://boba-nyc.datalife.nyc/
        * **Python Libraries**: [pandas](https://pandas.pydata.org/) | [streamlit](https://streamlit.io/) | [os](https://docs.python.org/3/library/os.html) | [pillow](https://pillow.readthedocs.io/en/stable/index.html)
        * **Data Sources**: [Yelp Fusion API - Business Search](https://www.yelp.com/developers/documentation/v3/business_search)
        * **Title Image**: [VIVI BUBBLE TEA - 49 Bayard St.](https://vivibubbletea.com/)
        
        ## References

        * [Streamlit Gallery](https://streamlit.io/gallery)
        * [Build 12 Data Science Apps with Python and Streamlit - Full Course | Author: Chanin Nantasenamat (dataprofessor) | Channel: freeCodeCamp.org](https://www.youtube.com/watch?v=JwSS70SZdyM)
        """
    )

store_counts_df = pd.read_csv(file_path + '/name_counts.csv', index_col = [0])
max_stores = int(store_counts_df['counts'].max())
default_store_count = 4

store_neighborhoods_df = pd.read_csv(file_path + '/store_neighborhoods.csv', index_col = [0])
neighborhoods_list = store_neighborhoods_df['ntaname'].unique()

## Sidebar - Select Options
st.sidebar.header('Select Options')

## Sidebar - Select Min # of Stores
store_count = st.sidebar.slider('Select Min # of Stores', 1, max_stores, default_store_count)

## Sidebar - Select Neighborhoods
selected_neighborhood = st.sidebar.multiselect('Select Neighborhoods', neighborhoods_list, neighborhoods_list)

def view_stores_by_count(count_of_stores):
    stores_df = store_counts_df[store_counts_df['counts'] >= store_count]
    stores_df = stores_df.rename(columns = {
        'name': 'Bubble Tea Shop Name',
        'counts': '# of Stores in 5 Boros',
    })
    stores_df.index += 1
    return stores_df

def view_stores_by_neighborhood(neighborhood):
    stores_df = store_neighborhoods_df[store_neighborhoods_df['ntaname'].isin(neighborhood)]
    return_stores_df = stores_df[[
        # 'id',
        'name',
        'boro_name',
        'ntaname',
        # 'url',
        'review_count', 
        'rating',
    ]]
    return_stores_df = return_stores_df.rename(columns = {
        'name': 'Bubble Tea Shop Name',
        'review_count': '# of Yelp Reviews',
        'rating': 'Average Rating',
        'boro_name': 'Borough',
        'ntaname': 'Neighborhood'
    })
    return_stores_df.sort_values(
        by = [
        'Borough',
        'Neighborhood',
        'Average Rating'
        ],
        ascending = [
            True,
            True,
            False
        ],
        inplace = True
    )
    return return_stores_df

stores_counts_df = view_stores_by_count(store_count)

stores_by_neighborhood_df = view_stores_by_neighborhood(selected_neighborhood)

st.subheader('Store Counts')
st.write(stores_counts_df)

fig = px.bar(stores_counts_df.sort_values('# of Stores in 5 Boros'), 
    y = 'Bubble Tea Shop Name',
    x = '# of Stores in 5 Boros',
    barmode = 'stack',
    orientation = 'h',
)
st.plotly_chart(fig)

st.write('---')

st.subheader('Store by Neighborhood')
st.write(stores_by_neighborhood_df)

# Horizontal Bar Chart
# https://plotly.com/python/horizontal-bar-charts/

