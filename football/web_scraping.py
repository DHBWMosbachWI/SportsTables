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
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/passing.htm")
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

    return result # returns dataframe

def get_player_rushing_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/rushing.htm")
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

    return result

def get_player_receiving_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/receiving.htm")
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

    return result

def get_player_scrimmage_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/scrimmage.htm")
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

    return result

def get_player_defense_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/defense.htm")
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

    return result

def get_all_nfl_teams(driver):
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

    return result  # returns list of dataframes due to multiple tables being used in given url

def get_all_stadiums(driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/stadiums/")
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

    return result

def get_team_defense_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/opp.htm")
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

    return result

def get_team_season_standings(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/")
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

    return result
