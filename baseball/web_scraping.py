import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def web_table_to_dataframe(web_table):
    """
    This function turns a html table into a pandas dataframe. 
    thead is used as column names of the dataframe and all rows under tbody are going into the dataframe rows.
    
    Args:
        web_table: html table as BeautifulSoup table object
        
    Return:
        df: pandas.DataFrame containing the content of the provided html table
    """
    header_row = web_table.find("thead")("tr")[-1]

    ## extract table header
    table_header = []
    for col_header in header_row:
        if col_header.name == "th":
            table_header.append(col_header.get_text().replace(" ", ""))
            
    # extract table content
    content_rows = web_table.find("tbody")("tr")
    content_data = []
    for content_row in content_rows:
        if len(table_header) != len(content_row):# "table header should be of same length as the table body row"
            continue
        row = []
        for data_cell in content_row:
            #print(data_cell.get_text())
            row.append(data_cell.get_text().strip())
        content_data.append([data_cell.get_text().strip() for data_cell in content_row])

    df = pd.DataFrame(content_data, columns=table_header)
    return df

def get_all_mlb_managers():
    response = requests.get(f"https://www.baseball-reference.com/managers/")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_all_mlb_teams():
    response = requests.get(f"https://www.baseball-reference.com/teams/")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_mlb_season_team_batting_stats(year:int):
    response = requests.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standard-batting.shtml")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_mlb_season_team_pitching_stats(year:int):
    response = requests.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standard-pitching.shtml")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_mlb_season_standings(year:int):
    response = requests.get(f"https://www.baseball-reference.com/leagues/majors/2022-standings.shtml")
    soup = BeautifulSoup(response.content, "html.parser")
    dataframes = []
    for i in range(0,6):
        dataframes.append(web_table_to_dataframe(soup("table")[i]))
        
    return pd.concat(dataframes, ignore_index=True)

def get_mlb_draft_player_bio(year:int):
    response = requests.get(f"https://www.baseball-reference.com/leagues/majors/{year}-debuts.shtml")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df