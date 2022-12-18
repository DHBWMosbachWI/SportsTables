# SportsTables
This repository cotains code & data to build the SportsTable corpus as described in our paper ''SportsTables: A new Corpus for Semantic Type Detection''. We do not provide the data (CSV files) itself, but all necessary python scripts to scrape the table data from the web.

## Structure
For each sport for which we scrape datatables from the web, a seperate folder is created. In each folder the following essential files are stored:
- metadata.json

Defines the mapping of each existing column header in a table to a semantic type.

- web_scraping.py

Contains the main python functions to scrape HTML tables from different specified web pages and transform the tables to Pandas-DataFrames

- web_scraping.ipynb

Jupyter-Notebook containing a cell, which uses the python functions from `web_scraping.py` and stores the returned Pandas-Dataframes to CSV-Files. Since the most sport data tables in the web are for a specific year(sport season), there is a `for year in range()` loop which iterates over all given years and scrape the HTML table for the respective year.

## Settings
In the `.env` file you have to set the `SportTables` environment variable, which defines the directory for storing the scraped HTML tables as CSV-Files. Since the necessary folder structure in the `SportTabled` directory is not yet created automatically during the scrape process, the folders for each sport must be created manually before executing the scrape scripts.



## Run the scraping process
For scraping the data tables from the web and build the SportsTable corpus, you have to execute each `web_scraping.ipynb` in each sport folder. The cell which must be executed in the notebook is marked with the heading ''Web-Scraping''.  