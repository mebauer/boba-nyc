# Obsessed with Boba? Analyzing Bubble Tea Shops in NYC Using the Yelp Fusion API

## Presenters

- Mark Bauer
- Chidi Ezeolu
- Ho Hsieh
- Nathan Williamson

## Event

[NYC Open Data Week 2022](https://www.open-data.nyc/)  

[Event RSVP](https://2022.open-data.nyc/event/obsessed-with-boba-analyzing-bubble-tea-shops-in-nyc-using-the-yelp-fusion-api/)  

- The ___notebooks___ can be found in the [teabook](https://github.com/mebauer/boba-nyc/tree/master/teabook) folder.

- The ___website___ for this repo can be found here: [boba-nyc.datalife.nyc](https://boba-nyc.datalife.nyc)

![cover-photo](teabook/busineses-per-neighborhood.png)

## Table of Contents

- [Introduction](#Introduction)
- [Prerequisites](#Prerequisites)
- [Data](#Data)
- [Analysis](#Analysis)
- [Open Source Applications Used in Project](#Open-Source-Applications-Used-in-Project)
- [Resources](#Resources)
- [Say Hello!](#Say-Hello)

## Introduction

In this workshop, we explore and develop insights about NYC's Bubble Tea Shops using the Yelp Fusion API. Sections include:

- How to use the Yelp Fusion API
- Data Cleaning, Wrangling and Visualizations in Python
- A demo of our web app created in Jupyter Book and Streamlit.

Additionally, questions we’ll explore include bubble tea locations, Yelp ratings, review counts and price.

After an initial introduction of each section, participants will join break-out groups depending on which topic they would like to learn more about. These break-out sessions will be hands-on and interactive. Participants will then reconvene for a Q&A and final thoughts. Attendees will gain a better understanding of the data analysis workflow and will leave with skills and a template to uncover insights with any dataset.

This workshop recommends beginner-level proficiency with Python and is focused on applying Python to data analysis; however, those new to Python are gladly welcome!

## Prerequisites

- Basics of Python or other programming languages (R, SQL, etc.)
- Basic knowledge of Data Analysis
- Basics of Jupyter Notebooks

This project recommends beginner-level proficiency with Python and is focused on applying Python to data analysis.

## Install

1. Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)

2. Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

3. Clone [boba-nyc](https://github.com/mebauer/boba-nyc) repo

    ```bash
    git clone https://github.com/mebauer/boba-nyc.git
    ```

4. Enter directory of local repo

    ```bash
    cd boba-nyc
    ```

5. Install requirements

    ```bash
    conda env create -f environment_detail.yml
    ```

## Other Commands

### Git

[Git - git-push Documentation](https://git-scm.com/docs/git-push)

```bash
git push origin
```

[Configuring a remote for a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-for-a-fork)

```bash
git remote -v
git remote add upstream https://github.com/mebauer/boba-nyc.git
git remote -v
```

[Syncing a fork from the command line](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork#syncing-a-fork-from-the-command-line)

_main_: name of local default branch  
_upstream/master_: name of remote parent (orginal) repo branch

```bash
git fetch upstream
git checkout main
git fetch upstream/master
```

### Jupyter Book

[Build your book](https://jupyterbook.org/start/build.html)

```bash
jupyter-book build --all teabook/
```

### Streamlit

[Create an app](https://docs.streamlit.io/library/get-started/create-an-app)

```bash
streamlit run <app.py>
```

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

You can view these notebooks through your browser by clicking _View_ under the _Static Webpage_ column.

| File Name | Description | Static Webpage |
| :-------- | :---------- | :------------- |
| [socrata-api-demo.ipynb](teabook/socrata-api-demo.ipynb) | Intro to the Socrata API with the NYC Dog Licensing Dataset & Python | [Demo](https://boba-nyc.datalife.nyc/socrata-api-demo.html) |
| [boba-analysis-nyc.ipynb](teabook/boba-analysis-nyc.ipynb) | Analyzing Bubble Tea shops in NYC. | [Demo](https://boba-nyc.datalife.nyc/boba-analysis-nyc.html) |
| [data-wrangling.ipynb](teabook/data-wrangling.ipynb) | Query and data cleaning workflow from the Yelp Fusion API's Business Search endpoint. | [Demo](https://boba-nyc.datalife.nyc/data-wrangling.html) |

## Open Source Applications Used in Project

- [Anaconda](https://www.anaconda.com/): A distribution of the Python and R programming languages for scientific computing (data science, machine learning applications, large-scale data processing, predictive analytics, etc.), that aims to simplify package management and deployment.  
- [Project Jupyter](https://jupyter.org/index.html): Project Jupyter is a non-profit, open-source project, born out of the IPython Project in 2014 as it evolved to support interactive data science and scientific computing across all programming languages.  
- [Jupyter Notebook](https://jupyter.org/try): The Jupyter Notebook is an open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text.  
- [Jupyter Book](https://jupyterbook.org): Jupyter Book is an open source project for building beautiful, publication-quality books and documents from computational material
- [nbviewer](https://nbviewer.jupyter.org/): A web application that lets you enter the URL of a Jupyter Notebook file, renders that notebook as a static HTML web page, and gives you a stable link to that page which you can share with others.  
- [Binder](https://mybinder.org/): The Binder Project is an open community that makes it possible to create sharable, interactive, reproducible environments.
- [Socrata](https://dev.socrata.com/): The Socrata Open Data API allows you to programmatically access a wealth of open data resources from governments, non-profits, and NGOs around the world.
- [Plotly](https://plotly.com/): The front end for ML and data science models.

## Other Applications and Services Used in Project

- [Google Cloud Storage](https://cloud.google.com/storage): Storage service used to host static website files.

### NYC Open Data Week 2022

- [About Open Data Week](https://2022.open-data.nyc/about/?_ga=2.50656297.1098322179.1641752075-1851954477.1641607907&_gl=1*1b9ycty*_ga*MTg1MTk1NDQ3Ny4xNjQxNjA3OTA3*_ga_7GQYNB09QV*MTY0MTc1NDU4My40LjAuMTY0MTc1NDU4My4w): Open Data Week is organized and produced by the NYC Open Data Program and BetaNYC. This annual festival  takes place during the first week of March to celebrate New York City’s Open Data Law, which was signed into law on March 7, 2012, and International Open Data Day which is typically the first Saturday in March.
- [NYC Open Data](https://opendata.cityofnewyork.us/): Open Data is free public data published by New York City agencies and other partners.

### Yelp Fusion API - references

- [Getting Started](https://www.yelp.com/developers/documentation/v3/get_started)  
- [Register for an API Key](https://www.yelp.com/developers/documentation/v3/authentication)
- [Business Endpoints](https://www.yelp.com/developers/documentation/v3/business)  
- [Samples on GitHub](https://github.com/Yelp/yelp-fusion)

### CC-licensed materials

- [File:Matcha green tea.jpg](https://commons.wikimedia.org/wiki/File:Matcha_green_tea.jpg) by [BubbleManiaCZ](https://commons.wikimedia.org/w/index.php?title=User:BubbleManiaCZ&action=edit&redlink=1) is under the [Creative Commons](https://en.wikipedia.org/wiki/en:Creative_Commons) [Attribution-Share Alike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/deed.en) license.

### Cheatsheets

- [Git](https://intellipaat.com/mediaFiles/2019/03/Git-Cheat-Sheet.jpg)

- [Conda](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)

### Image editors

- [Favicon Generator / Generate from Image](https://favicon.io/favicon-converter/)

### Social media badges

- [Shields.io: Quality metadata for open source projects](https://shields.io/)

## Further Reading

### Licensing

- [Best practices for attribution](https://wiki.creativecommons.org/wiki/best_practices_for_attribution)
- [Commons:Credit line](https://commons.wikimedia.org/wiki/Commons:Credit_line)

## Say Hello 👋

We can be reached at:

| Presenter | LinkedIn | GitHub | Twitter |
| --------- | -------- | ------ | ------- |
| Mark Bauer | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/markebauer) | [![GitHub followers](https://img.shields.io/github/followers/mebauer?style=social)](https://github.com/mebauer) | [![Twitter Follow](https://img.shields.io/twitter/follow/markbauerwater?style=social)](https://twitter.com/markbauerwater) |
| Chidi Ezeolu | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/chidi-ezeolu-411b0856) | [![GitHub followers](https://img.shields.io/github/followers/datalifenyc?style=social)](https://github.com/datalifenyc)| |
| Ho Hsieh | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/hohsieh/) | [![GitHub followers](https://img.shields.io/github/followers/hohsieh?style=social)](https://github.com/hohsieh) | |
| Nathan Williamson | | [![GitHub followers](https://img.shields.io/github/followers/nateswill?style=social)](https://github.com/nateswill) | |
