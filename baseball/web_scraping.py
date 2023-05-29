import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By


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

def get_all_mlb_managers(driver):

    result = None
    driver.get(f"https://www.baseball-reference.com/managers/")
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


def get_all_mlb_teams(driver):

    result = None
    driver.get(f"https://www.baseball-reference.com/teams/")
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

    return result # returns dataframe
def get_mlb_season_team_batting_stats(year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standard-batting.shtml")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        dfs = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)

        result = dfs
        print(dfs)
    except:
        print("not possible")
        pass

    return result # returns dataframe

#FEHLENDE LINKS TABELLEN
def get_mlb_season_team_batting_League_Baserunning (year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-baserunning-batting.shtml")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        dfs = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)

        result = dfs
        print(dfs)
    except:
        print("not possible")
        pass

    return result # returns dataframe

def get_mlb_season_team_batting_value (year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-value-batting.shtml")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        dfs = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)

        result = dfs
        print(dfs)
    except:
        print("not possible")
        pass

    return result # returns dataframe


def get_mlb_season_team_cumulative_batting (year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-cumulative-batting.shtml")

    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        dfs = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)

        result = dfs
        print(dfs)
    except:
        print("not possible")
        pass

    return result # returns dataframe

def get_mlb_season_team_probabaility_batting (year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-win_probability-batting.shtml")

    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        dfs = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)

        result = dfs
        print(dfs)
    except:
        print("not possible")
        pass

    return result # returns dataframe


def get_mlb_season_team_laegue_ratio_batting (year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-ratio-batting.shtml")

    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        dfs = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)

        result = dfs
        print(dfs)
    except:
        print("not possible")
        pass

    return result # returns dataframe

def get_mlb_season_team_compare (year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/team_compare.cgi?lg=MLB&year={year}")


    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        dfs = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)

        result = dfs
        print(dfs)
    except:
        print("not possible")
        pass

    return result # returns dataframe

def get_mlb_season_team_pitching_stats(year:int, driver):

    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standard-pitching.shtml")
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

    return result # returns dataframe

def get_mlb_season_team_starter_pitching(year:int, driver):



    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-starter-pitching.shtml")
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

    return result # returns dataframe

def get_mlb_season_team_minors_pitching(year:int, driver):



    result = None
    driver.get(f"https://www.baseball-reference.com/register/leader.cgi?type=pitch&year={year}")
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

    return result # returns dataframe

def get_mlb_season_team_value_pitching(year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-value-pitching.shtml")
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

    return result # returns dataframe

def get_mlb_season_cumulutive_pitching(year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-cumulative-pitching.shtml")
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

    return result # returns dataframe

def get_mlb_season_ration_pitching(year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-ratio-pitching.shtml")
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

    return result # returns dataframe

def get_mlb_season_neutr_pitching(year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-neutral-pitching.shtml")
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

    return result # returns dataframe

def get_mlb_season_basesituation_pitching (year:int, driver):

    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-basesituation-pitching.shtml")
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

    return result # returns dataframe

def get_mlb_season_standings(year:int, driver):
    '''response = requests.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standings.shtml")
    soup = BeautifulSoup(response.content, "html.parser")
    dataframes = []
    for i in range(0,6):
        dataframes.append(web_table_to_dataframe(soup("table")[i]))
        
    return pd.concat(dataframes, ignore_index=True)'''

    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standings.shtml")
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

    return result # returns dataframe

#Added new function. The last one was only for 2022 which results in 20 identical csv files.
#From 1994 until 1999 there are 6 charts to put together. Before there are only 4.
def get_mlb_season_standing(year:int, driver):
    '''response = requests.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standings.shtml")
    soup = BeautifulSoup(response.content, "html.parser")
    dataframes = []
    for i in range(0,4):
        dataframes.append(web_table_to_dataframe(soup("table")[i]))

    return pd.concat(dataframes, ignore_index=True)'''

    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standings.shtml")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table") # 4 tabellen nehmen und zu einer hinzufügen; for table in tables
        df = None
        dfs = []

        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)
        result = dfs

    except:
        print("not possible")
        pass

    return result # returns dataframe


def get_mlb_season_standing_RANGE_4(year:int, driver):
    '''response = requests.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standings.shtml")
    soup = BeautifulSoup(response.content, "html.parser")
    dataframes = []
    for i in range(0,4):
        dataframes.append(web_table_to_dataframe(soup("table")[i]))

    return pd.concat(dataframes, ignore_index=True)'''

    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standings.shtml")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = None
        dfs = []

        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dfs.append(df)
        result = dfs

    except:
        print("not possible")
        pass

    return result # returns dataframe

def get_mlb_season_standings_RANGE_6(year:int, driver):
    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-standings.shtml")
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

    return result # returns dataframe


def get_mlb_draft_player_bio(year:int, driver):


    result = None
    driver.get(f"https://www.baseball-reference.com/leagues/majors/{year}-debuts.shtml")
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

    return result # returns dataframe

#%%

#%%
