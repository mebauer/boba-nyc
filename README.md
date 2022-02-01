# Searching for Boba: Analyzing Bubble Tea Shops in NYC Using the Yelp Fusion API

__Presenters__: Mark Bauer, Nathan Williamson, Chidi Ezeolu  
__Event__: NYC Open Data Week 2022  
__Details__: https://www.open-data.nyc/  

The analysis can be found in the [boba-analysis-nyc.ipynb](https://github.com/mebauer/boba-nyc/blob/master/teabook/boba-analysis-nyc.ipynb) notebook. 

![cover-photo](busineses-per-neighborhood.png)

## Table of Contents

* [Introduction](#Introduction)
* [Prerequisites](#Prerequisites)
* [Data](#Data)
* [Analysis](#Analysis)
* [Open Source Applications Used in Project](#Open-Source-Applications-Used-in-Project)
* [Resources](#Resources)
* [Say Hello!](#Say-Hello)

## Introduction

TBD...

In this project, I explore NYC's Bubble Tea Shops using the Yelp Fusion API. Specifically, I attempt to answer the following questions:

1. TBD
2. TBD
3. TBD  
4. TBD  

## Prerequisites

* Basics of Python or other programming languages (R, SQL, etc.)
* Knowledge of Data Analysis
* Basics of Jupyter Notebooks

This project recommends beginner-level proficiency with Python and is focused on applying Python to data analysis.

## Data

### Yelp Fusion API

Note: the Yelp Fusion API is a __free__ API on Yelp's Developer Site. Details from the Yelp Fusion page:

> __Create an app on Yelp's Developers site__
In order to set up your access to Yelp Fusion API, you need to create an app with Yelp. This app represents the application you'll build using our API and includes the credentials you'll need to gain access. Here are the steps for creating an app:  
>
> 1. Go to [Create App](https://www.yelp.com/developers/v3/manage_app)  
> 2. In the create new app form, enter information about your app, then agree to Yelp API Terms of Use and Display Requirements. Then click the Submit button.  
> 3. You will now have an API Key.  
>
> __Please keep the API Key 🔑 to yourself since it is the credential for your call to Yelp's API.__  

Source: [Get started with the Yelp Fusion API](https://www.yelp.com/developers/documentation/v3/get_started)

### Datasets

| Dataset | Description |
| :-------- | :---------- |
| [Yelp Fusion API - Business Search](https://www.yelp.com/developers/documentation/v3/business_search) | This endpoint returns up to 1000 businesses based on the provided search criteria. |
| [NYC Borough Boundaries](https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm) | GIS data of NYC boroughs. |

### Output Data

The output data retrieved from the Yelp Fusion API query is titled [boba-nyc.csv](https://github.com/mebauer/boba-nyc/blob/master/boba-nyc.csv) and is saved as a CSV file.

## Analysis

You can view these notebooks through your browser by clicking *View* under the *Static Webpage* column. 

| File Name | Description | Static Webpage |
| :-------- | :---------- | :------------- |
| [boba-analysis-nyc.ipynb](https://github.com/mebauer/boba-nyc/blob/master/boba-analysis-nyc.ipynb) | Analyzing Bubble Tea shops in NYC. | [TBD](TBD) |
| [data-wrangling.ipynb](https://github.com/mebauer/boba-nyc/blob/master/data-wrangling.ipynb) | Query and data cleaning workflow from the Yelp Fusion API's Business Search endpoint. | [TBD](TBD) |

## Open Source Applications Used in Project

- [Anaconda](https://www.anaconda.com/): A distribution of the Python and R programming languages for scientific computing (data science, machine learning applications, large-scale data processing, predictive analytics, etc.), that aims to simplify package management and deployment.  
- [Project Jupyter](https://jupyter.org/index.html): Project Jupyter is a non-profit, open-source project, born out of the IPython Project in 2014 as it evolved to support interactive data science and scientific computing across all programming languages.  
- [Jupyter Notebook](https://jupyter.org/try): The Jupyter Notebook is an open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text.  
- [nbviewer](https://nbviewer.jupyter.org/): A web application that lets you enter the URL of a Jupyter Notebook file, renders that notebook as a static HTML web page, and gives you a stable link to that page which you can share with others.  
- [Binder](https://mybinder.org/): The Binder Project is an open community that makes it possible to create sharable, interactive, reproducible environments.

## Resources

NYC Open Data Week 2022:
- [About Open Data Week](https://2022.open-data.nyc/about/?_ga=2.50656297.1098322179.1641752075-1851954477.1641607907&_gl=1*1b9ycty*_ga*MTg1MTk1NDQ3Ny4xNjQxNjA3OTA3*_ga_7GQYNB09QV*MTY0MTc1NDU4My40LjAuMTY0MTc1NDU4My4w): Open Data Week is organized and produced by the NYC Open Data Program and BetaNYC. This annual festival  takes place during the first week of March to celebrate New York City’s Open Data Law, which was signed into law on March 7, 2012, and International Open Data Day which is typically the first Saturday in March.   
- [NYC Open Data](https://opendata.cityofnewyork.us/): Open Data is free public data published by New York City agencies and other partners. 

Yelp Fusion API:  
- [Getting Started](https://www.yelp.com/developers/documentation/v3/get_started)  
- [Register for an API Key](https://www.yelp.com/developers/documentation/v3/authentication) 
- [Business Endpoints](https://www.yelp.com/developers/documentation/v3/business)  
- [Samples on GitHub](https://github.com/Yelp/yelp-fusion)

## Further Reading

TBD


## Say Hello!   

I can be reached at:  

Twitter | [markbauerwater](https://twitter.com/markbauerwater)  
LinkedIn | [markebauer](https://www.linkedin.com/in/markebauer/)  
GitHub | [mebauer](https://github.com/mebauer)
