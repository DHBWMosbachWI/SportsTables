import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    # extract table header
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

def check_tables(result):
    if type(result) == list:
        new_result = []
        for table in range(len(result)):
            if result[table].iloc[0].to_string().startswith('Unnamed'):
                result[table].columns = result[table].columns.droplevel(0)
            columns = list(result[table].columns)
            #new_result.append(result[table][result[table].Rk.str.contains(columns[0]) is False])
            new_result.append(result[table].loc[result[table][columns[0]] != columns[0]])
    else:
        if result.iloc[0].to_string().startswith('Unnamed'): # check if multiple headers
            result.columns = result.columns.droplevel(0) # drop first layer
        columns = list(result.columns)
        #new_result = result[result.Rk.str.contains(columns[0]) is False] # delete rows that are like header
        new_result = result.loc[result[columns[0]] != columns[0]]
    return new_result

def get_nba_season_team_stats(year:int, driver):

    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}.html")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df.append(pd.read_html(html)[0])
        result = df
    except:
        print("not possible")
        pass

    return check_tables(result)

def get_nba_season_all_nba(year:int, driver):

    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}.html")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = []
        dataframes =[]

        for i in range (72,74):
            html = tables[i].get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dataframes.append(df)
        result = pd.concat(dataframes, ignore_index=True)
    except:
        print("not possible")
        pass

    return result

def get_nba_season_all_defensive(year:int, driver):

    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}.html")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = []
        dataframes =[]

        for i in range (74,76):
            html = tables[i].get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dataframes.append(df)
        result = pd.concat(dataframes, ignore_index=True)
    except:
        print("not possible")
        pass

    return check_tables(result)


def get_nba_season_all_star_game_rosters(year:int, driver):

    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}.html")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = []
        dataframes =[]

        for i in range (77,79):
            html = tables[i].get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dataframes.append(df)
        result = pd.concat(dataframes, ignore_index=True)
    except:
        print("not possible")
        pass

    return check_tables(result)
def get_nba_season_standing(year:int, driver):
    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = []
        dataframes =[]

        for i in range (0,2):
            html = tables[i].get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dataframes.append(df)
        result = pd.concat(dataframes, ignore_index=True)

    except:
        print("not possible")
        pass

    return check_tables(result)

def get_nba_season_standings(year:int, driver):
    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = []
        dataframes =[]
        for i in range(2,4):
            html = tables[i].get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dataframes.append(df)
        result = dataframes
    except:
        print("not possible")
        pass

    return check_tables(result)

def get_nba_player_stats(year:int, driver):

    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html")
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

    return check_tables(result)


def get_nba_coaches_stats(year:int, driver):

    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_coaches.html")
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

#zusätzliche Tabellen

def get_nba_player_Per_36_Minutes(year:int, driver):
    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_per_minute.html")
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

    return check_tables(result)
def get_nba_player_Per_100_Poss(year:int, driver):
    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_per_poss.html")
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

    return check_tables(result)

def get_nba_Advanced(year:int, driver):
    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html")
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

    return check_tables(result)

def get_nba_Adjusted_Shooting(year:int, driver):
    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_adj_shooting.html")
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

    return check_tables(result)

def get_nba_Rookies(year:int, driver):
    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_rookies.html")
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

    return check_tables(result)

def get_nba_62_Players(year:int, driver):
    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_final.html")
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

    return check_tables(result)

def get_nba_team_rating(year:int, driver):
    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html")
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

    return check_tables(result)

def get_nba_Eastern_Conference(year:int, driver):

    result = None
    driver.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_standings_by_date_eastern_conference.html")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = []
        for table in tables:
            html = table.get_attribute("outerHTML")
            df.append(pd.read_html(html)[0])
        result = df
    except:
        print("not possible")
        pass

    return check_tables(result)

#%%

#%%

#%%
