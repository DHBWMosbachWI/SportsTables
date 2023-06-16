import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time



def close_popups(driver):
    """
    This function closes disruptive pop ups
    Args:
        driver: the driver the user needs

    Returns:
        None
    """
    try:
        WebDriverWait(driver,1000).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-47sehv"))).click() # close privacy pop up
        time.sleep(3)
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
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/passing.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

    return check_tables(result) # returns dataframe

def get_player_rushing_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/rushing.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

def get_player_receiving_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/receiving.htm")

    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

def get_player_scrimmage_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/scrimmage.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

def get_player_defense_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/defense.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/kicking.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

def get_player_punting_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/punting.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

def get_player_return_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/returns.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

def get_player_scoring_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/scoring.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

def get_all_nfl_teams(driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/teams/")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

    return check_tables(result)  # returns list of dataframes due to multiple tables being used in given url

def get_all_stadiums(driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/stadiums/")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

def get_team_defense_stats(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/opp.htm")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

    return check_tables(result)

def get_team_season_standings(year:int, driver):
    result = None
    driver.get(f"https://www.pro-football-reference.com/years/{year}/")
    if driver.find_element(By.ID, "modal-container").is_displayed():
        close_popups(driver)
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

    return check_tables(result)
