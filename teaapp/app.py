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

    ## About

    Analyzing Bubble Tea Shops in NYC

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
