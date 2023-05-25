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

def get_nhl_season_standings(year:int, driver): #zwei ersten tabellen zusammengefügt

    result = None
    driver.get(f"https://www.hockey-reference.com/leagues/NHL_{year}.html")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = []
        dataframes =[]

        for i in range(0,2):
            html = tables[i].get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dataframes.append(df)
        result = pd.concat(dataframes, ignore_index=True)

    except:
        print("not possible")
        pass

    return result

def get_nhl_season_standings_zusatz(year:int, driver): # die restliche minitabellen erstellen

    result = None
    driver.get(f"https://www.hockey-reference.com/leagues/NHL_{year}.html")
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        df = []
        dataframes =[]

        for i in range(2, 60):
            html = tables[i].get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            dataframes.append(df)
        result = dataframes

    except:
        print("not possible")
        pass

    return result

#FEHLENDE LINKS TABELLEN
def get_nhl_hat_tricks (year:int, driver):
    ''' response = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html")
      soup = BeautifulSoup(response.content, "html.parser")
      df = web_table_to_dataframe(soup("table")[0])
      return df
    '''

    result = None
    driver.get(f"hockey-reference.com/leagues/NHL_{year}_hat-tricks.html")

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
def get_nhl_penalty_shots(year:int, driver):
    ''' response = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html")
      soup = BeautifulSoup(response.content, "html.parser")
      df = web_table_to_dataframe(soup("table")[0])
      return df
    '''

    result = None
    driver.get(f"www.hockey-reference.com/leagues/NHL_{year}_penalty-shots.html")


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

def get_nhl_debuts (year:int, driver):
    ''' response = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html")
      soup = BeautifulSoup(response.content, "html.parser")
      df = web_table_to_dataframe(soup("table")[0])
      return df
    '''

    result = None
    driver.get(f"hockey-reference.com/leagues/NHL_{year}_debut.html")
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

def get_nhl_final_season (year:int, driver):
    ''' response = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html")
      soup = BeautifulSoup(response.content, "html.parser")
      df = web_table_to_dataframe(soup("table")[0])
      return df
    '''

    result = None
    driver.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_final.html")
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

def get_nhl_births (year:int, driver):
    ''' response = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html")
      soup = BeautifulSoup(response.content, "html.parser")
      df = web_table_to_dataframe(soup("table")[0])
      return df
    '''

    result = None
    driver.get(f"www.hockey-reference.com/leagues/NHL_{year}_births.html")

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

def get_nhl_deaths (year:int, driver):
    ''' response = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html")
      soup = BeautifulSoup(response.content, "html.parser")
      df = web_table_to_dataframe(soup("table")[0])
      return df
    '''

    result = None
    driver.get(f"www.hockey-reference.com/leagues/NHL_{year}_deaths.html")
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
#added
def get_all_nhl_teams(driver):

    '''response = requests.get(f"https://www.hockey-reference.com/teams/")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df'''

    result = None
    driver.get(f"https://www.hockey-reference.com/teams/")
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

def get_nhl_player_stats(year:int, driver):
    ''' response = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html")
      soup = BeautifulSoup(response.content, "html.parser")
      df = web_table_to_dataframe(soup("table")[0])
      return df
    '''

    result = None
    driver.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html")
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


def get_nhl_player_goalie_stats(year:int, driver):
    '''response = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_goalies.html")
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df'''

    result = None
    driver.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html")
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

def get_nhl_playoff_standings(year:int, driver):
    '''response = requests.get(f"https://www.hockey-reference.com/playoffs/NHL_{year}.html")
      soup = BeautifulSoup(response.content, "html.parser")
      if year == 2020:
          df = web_table_to_dataframe(soup("table")[25])
      else:
          df = web_table_to_dataframe(soup("table")[16])
      return df'''
    result = None
    driver.get(f"https://www.hockey-reference.com/playoffs/NHL_{year}.html")

    tables = driver.find_elements(By.TAG_NAME, "table")
    dfs = []

    for table in tables:
        html = table.get_attribute("outerHTML")
        if year == 2020:
            df = pd.read_html(html)
            dfs.append(df[0])
        else:
            df = pd.read_html(html)
            dfs.append(df[0])
    result = dfs
    return result

def get_nhl_playoff_player_stats(year:int, driver):
    '''response = requests.get(f"https://www.hockey-reference.com/playoffs/NHL_{year}_skaters.html")
      soup = BeautifulSoup(response.content, "html.parser")
      df = web_table_to_dataframe(soup("table")[0])
      return df
    '''

    result = None
    driver.get(f"https://www.hockey-reference.com/playoffs/NHL_{year}_skaters.html")
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
def get_nhl_playoff_player_goalies_stats(year:int, driver):
    '''response = requests.get(f"https://www.hockey-reference.com/playoffs/NHL_{year}_goalies.html")
      soup = BeautifulSoup(response.content, "html.parser")
      df = web_table_to_dataframe(soup("table")[0])
      return df
    '''
    result = None
    driver.get(f"https://www.hockey-reference.com/playoffs/NHL_{year}_goalies.html")
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

  #%%

#%%

#%%

#%%
