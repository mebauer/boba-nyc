# Import Libraries

## External Libraries
import pandas as pd
import streamlit as st
import os
from PIL import Image

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

st.sidebar.header('Select Options')
store_count = st.sidebar.slider('Select Min # of Stores', 1, max_stores, default_store_count)

def view_stores_by_count(count_of_stores):
    stores_df = store_counts_df[store_counts_df['counts'] >= store_count]
    stores_df = stores_df.rename(columns = {
        'name': 'Bubble Tea Shop Name',
        'counts': '# of Stores in 5 Boros',
    })
    stores_df.index += 1
    return stores_df

# def user_options():
#     store_count = st.sidebar.slider('# of Stores', 1, max_stores, default_store_count)
#     data = {
#         'store_count': store_count,
#     }
#     options = pd.DataFrame(data, index = [0])
#     return options

stores_counts_df = view_stores_by_count(store_count)

st.subheader('Store Counts')
st.write(stores_counts_df)