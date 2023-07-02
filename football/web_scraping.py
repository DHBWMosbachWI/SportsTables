import os
from os.path import join

import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def safe_csv(df, filename):
    try:
        df.to_csv(join(os.environ["SportsTables"], "football", filename), index=False)
        print(f'Saved {filename}')
    except Exception as e:
        print('could not safe csv file')
        print(e)

def close_popups(driver):
    """
    This function closes disruptive pop up's
    Args:
        driver: the driver the user needs

    Returns:
        None
    """
    try:
        WebDriverWait(driver,1000).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-47sehv"))).click() # close privacy pop up
        time.sleep(5)
        WebDriverWait(driver,1000).until(EC.element_to_be_clickable((By.CLASS_NAME, "closer"))).click() # close pop up
    except Exception as e:
        print(e)
    pass

def web_table_to_dataframe(web_table): # remove?
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
    driver.get(f"https://www.pro-football-reference.com/years/{year}/passing.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "passing")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_season_player_passing_stats_{year}.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_player_rushing_stats(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/rushing.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "rushing")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_season_player_rushing_stats_{year}.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_player_receiving_stats(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/receiving.htm")

    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "receiving")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_season_player_receiving_stats_{year}.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_player_scrimmage_stats(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/scrimmage.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "receiving_and_rushing")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_season_player_scrimmage_stats_{year}.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_player_defense_stats(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/defense.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "defense")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_season_player_defense_stats_{year}.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def check_tables(result):
    if type(result) == list: #result can be single df or a list of df
        new_result = []
        for table in range(len(result)):
            if result[table].columns.nlevels > 1: # are there more than one header level?
                n_level = result[table].columns.nlevels-1
                for index in range(n_level):
                    result[table].columns = result[table].columns.droplevel(0) # remove first header until only one is left
            columns = list(result[table].columns)
            new_result.append(result[table].loc[result[table][columns[0]] != columns[0]])
            # are headers repeated as rows? Remove these
    else:
        if result.columns.nlevels > 1:
            n_level = result.columns.nlevels-1
            for index in range(n_level):
                result.columns = result.columns.droplevel(0) # drop first layer
        columns = list(result.columns)
        new_result = result.loc[result[columns[0]] != columns[0]]
    return new_result

def get_player_kicking_stats(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/kicking.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "kicking")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_season_player_kicking_stats_{year}.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_player_punting_stats(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/punting.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "punting")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_season_player_punting_stats_{year}.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_player_return_stats(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/returns.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "returns")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_season_player_return_stats_{year}.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_player_scoring_stats(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/scoring.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "scoring")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_season_player_scoring_stats_{year}.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_all_nfl_teams(driver):
    driver.get(f"https://www.pro-football-reference.com/teams/")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        for title in ['teams_active', 'teams_inactive']:
            table = driver.find_element(By.ID, title) # find by tag table doesn't work
            html = table.get_attribute("outerHTML")
            df = check_tables(pd.read_html(html)[0])
            filename = f'nfl_all_{title}_franchises.csv'
            safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_all_stadiums(driver):
    driver.get(f"https://www.pro-football-reference.com/stadiums/")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        table = driver.find_element(By.ID, "stadiums")
        html = table.get_attribute("outerHTML")
        df = check_tables(pd.read_html(html)[0])
        filename = f'nfl_all_stadiums.csv'
        safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_team_defense_stats(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/opp.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        for title in ['team_stats', 'passing', 'rushing', 'returns', 'kicking', 'punting', 'team_scoring', 'team_conversions']:
            table = driver.find_element(By.ID, title)
            html = table.get_attribute("outerHTML")
            df = check_tables(pd.read_html(html)[0])
            # corrections of title
            if title == 'team_stats':
                title = 'defense'
            if title.startswith('team'):
                title = title.split('_')[1]
            if title in ['returns', 'kicking', 'punting', 'conversions']:
                title = f'{title}_against'
            if title in ['passing', 'rushing', 'scoring']:
                title = f'{title}_defense'
            filename = f'nfl_season_team_{title}_stats_{year}.csv'
            safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_team_season_standings(year:int, driver):
    driver.get(f"https://www.pro-football-reference.com/years/{year}/")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
    try:
        for title in ['AFC', 'NFC', 'playoff_results', 'team_stats', 'passing', 'rushing', 'returns', 'kicking',
                      'punting', 'team_scoring', 'team_conversions']:
            table = driver.find_element(By.ID, title)
            html = table.get_attribute("outerHTML")
            df = check_tables(pd.read_html(html)[0])
            # corrections of title
            if title == 'team_stats':
                title = 'offense'
            if title.startswith('team'):
                title = title.split('_')[1]
            if title in ['passing', 'rushing', 'scoring']:
                title = f'{title}_offense'
            if title in ['AFC', 'NFC']:
                filename = f'nfl_season_team_{title.lower()}_standings_{year}.csv'
            else:
                filename = f'nfl_season_team_{title}_stats_{year}.csv'
            safe_csv(df, filename)
    except Exception as e:
        print("not possible")
        print(e)
        pass
