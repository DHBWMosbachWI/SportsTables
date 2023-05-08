import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
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

def get_player_passing_stats(year:int, driver):
    '''
    response = requests.get(f"https://www.pro-football-reference.com/years/{year}/passing.htm")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df
    '''

    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/passing.htm")
    # Code von Jule
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = None

        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]

        result = df
    except:
        print("not possible")
        pass

    return result # gibt ein dataframe zurück da nur eine Tabelle auf Seite

def get_player_rushing_stats(year:int):
    response = requests.get(f"https://www.pro-football-reference.com/years/{year}/rushing.htm")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_player_receiving_stats(year:int):
    response = requests.get(f"https://www.pro-football-reference.com/years/{year}/receiving.htm")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_player_scrimmage_stats(year:int):
    response = requests.get(f"https://www.pro-football-reference.com/years/{year}/scrimmage.htm")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_player_defense_stats(year:int):
    response = requests.get(f"https://www.pro-football-reference.com/years/{year}/defense.htm")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_all_nfl_teams(driver):
    '''
    response = requests.get(f"https://www.pro-football-reference.com/teams/")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df
    '''

    result = None
    driver.get(f"https://www.pro-football-reference.com/teams/")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")

        dfs = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)

        result = dfs
    except:
        print("not possible")
        pass

    return result # gibt Liste mit allen dataframes zurück, da mehrere Tabellen auf Seite

def get_all_stadiums():
    response = requests.get(f"https://www.pro-football-reference.com/stadiums/")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_team_defense_stats(year:int):
    response = requests.get(f"https://www.pro-football-reference.com/years/{year}/opp.htm")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df

def get_team_season_standings(year:int):
    response = requests.get(f"https://www.pro-football-reference.com/years/{year}/")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    df2 = web_table_to_dataframe(soup("table")[1])
    
    return pd.concat([df, df2], ignore_index=True)