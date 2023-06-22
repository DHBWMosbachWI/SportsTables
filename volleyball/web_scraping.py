import os
from os.path import join

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re
from selenium.webdriver.support.select import Select


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
        if len(table_header) != len(content_row):  # "table header should be of same length as the table body row"
            continue
        row = []
        for data_cell in content_row:
            # print(data_cell.get_text())
            row.append(data_cell.get_text().strip())
        content_data.append([data_cell.get_text().strip() for data_cell in content_row])

    df = pd.DataFrame(content_data, columns=table_header)
    return df


def check_tables(result):
    if type(result) == list:  # result can be single df or a list of df
        new_result = []
        for table in range(len(result)):
            if result[table].columns.nlevels > 1:  # are there more than one header level?
                n_level = result[table].columns.nlevels - 1
                for index in range(n_level):
                    result[table].columns = result[table].columns.droplevel(
                        0)  # remove first header until only one is left
            columns = list(result[table].columns)
            new_result.append(result[table].loc[result[table][columns[0]] != columns[0]])
            # are headers repeated as rows? Remove these!
    else:
        if result.columns.nlevels > 1:
            n_level = result.columns.nlevels - 1
            for index in range(n_level):
                result.columns = result.columns.droplevel(0)  # drop first layer
        columns = list(result.columns)
        new_result = result.loc[result[columns[0]] != columns[0]]
        if result.columns[0] == 0:  # anomalies in team stats
            result.columns = result.iloc[3]
            new_result = result.iloc[4:]
    return new_result


def get_volleyball_league_scores_bundesliga_men(year, driver):
    url = f'https://www.volleyball-bundesliga.de/cms/home/1_bundesliga_maenner/archiv/statistikrankings/saison_{year}_{year + 1 - 2000}.xhtml'
    driver.get(url)
    time.sleep(5)
    while True:
        try:
            button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[1]")
            button.click()

        except:
            break
    try:
        dropdown = driver.find_element(By.XPATH,
                                       "/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[2]/form/div/div[2]/div/div/div[1]/select")
        select = Select(dropdown)
        select.select_by_visible_text("100")
        time.sleep(7)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all('table')
        for i, table in enumerate(tables):
            h1_tag = table.find_previous('h1')
            title = re.sub(r'[^\w\s-]', '', h1_tag.text.strip())
            title = title.lower()
            df = pd.read_html(str(table))[0]
            df = check_tables(df)
            filename = f'volleyball_{title.replace(" ", "_").replace("  ", "_")}_{year}_{year + 1}.csv'
            df.to_csv(filename, index=False)
            print(f'Saved {filename}')

    except Exception as e:
        print("not possible")
        print(e)
        pass


def get_volleyball_league_scores_bundesliga_women(year, driver):
    url = f'https://www.volleyball-bundesliga.de/cms/home/1_bundesliga_frauen/archiv/statistikrankings/saison_{year}_{year + 1 - 2000}.xhtml'
    driver.get(url)
    time.sleep(5)
    while True:
        try:
            button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[1]")
            button.click()
        except:
            break
    try:
        dropdown = driver.find_element(By.XPATH,
                                       "/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[2]/form/div/div[2]/div/div/div[1]/select")
        select = Select(dropdown)
        select.select_by_visible_text("100")
        time.sleep(7)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all('table')
        for i, table in enumerate(tables):
            h1_tag = table.find_previous('h1')
            title = re.sub(r'[^\w\s-]', '', h1_tag.text.strip())
            title = title.lower()
            df = pd.read_html(str(table))[0]
            df = check_tables(df)
            filename = f'volleyball_{title.replace(" ", "_").replace("  ", "_")}_{year}_{year + 1}.csv'
            df.to_csv(filename, index=False)
            print(f'Saved {filename}')

    except Exception as e:
        print("not possible")
        print(e)
        pass


def safe_csv(df, filename):
    try:
        df.to_csv(join(os.environ["SportsTables"], "volleyball", filename), index=False)
        print(f'Saved {filename}')
    except Exception as e:
        print('could not safe csv file')
        print(e)


def get_championsleague_women(year, driver):
    try:  # first load the website of the given year
        driver.get(f'https://www-old.cev.eu/Competition-Area/History.aspx?ID=1262')  # contains table with all years
        link = driver.find_element(By.PARTIAL_LINK_TEXT, f'{year}').get_attribute('href')
        driver.get(link)
        # it's not possible to use the click() function, therefore you have to get the url and use driver.get()
    except Exception as e:
        print('could not load given year!')
        print(e)
    league = f'volleyball_championsleague_women'
    get_team_standings(year, driver, league)
    get_team_stats(year, driver, league)
    get_player_stats(year, driver, league)


def get_championsleague_men(year, driver):
    try:
        driver.get(f'https://www-old.cev.eu/Competition-Area/History.aspx?ID=1259')  # contains table with all years
        link = driver.find_element(By.PARTIAL_LINK_TEXT, f'{year}').get_attribute('href')
        driver.get(link)
        # it's not possible to use the click() function, therefore you have to get the url and use driver.get()
    except Exception as e:
        print('could not load given year!')
        print(e)
    league = f'volleyball_championsleague_men'
    get_team_standings(year, driver, league)
    get_team_stats(year, driver, league)
    get_player_stats(year, driver, league)


def get_cev_cup_men(year, driver):
    if year < 2012:  # inconsistent writing of the year
        year = year - 1
    try:
        driver.get(f'https://www-old.cev.eu/Competition-Area/History.aspx?ID=1260')  # contains table with all years
        link = driver.find_element(By.PARTIAL_LINK_TEXT, f'{year}').get_attribute('href')
        driver.get(link)
        # it's not possible to use the click() function, therefore you have to get the url and use driver.get()
    except Exception as e:
        print('could not load given year!')
        print(e)
    if year < 2012:  # redo year so filename is correct
        year = year + 1
    league = f'volleyball_cev_cup_men'
    get_team_standings(year, driver, league)
    get_team_stats(year, driver, league)
    get_player_stats(year, driver, league)


def get_cev_cup_women(year, driver):
    if year < 2012:  # inconsistent writing of the year
        year = year - 1
    try:
        driver.get(f'https://www-old.cev.eu/Competition-Area/History.aspx?ID=5')  # contains table with all years
        link = driver.find_element(By.PARTIAL_LINK_TEXT, f'{year}').get_attribute('href')
        driver.get(link)
        # it's not possible to use the click() function, therefore you have to get the url and use driver.get()
    except Exception as e:
        print('could not load given year!')
        print(e)
    if year < 2012:  # redo year so filename is correct
        year = year + 1
    league = f'volleyball_cev_cup_women'
    get_team_standings(year, driver, league)
    get_team_stats(year, driver, league)
    get_player_stats(year, driver, league)


def get_golden_league_men(year, driver):
    try:
        driver.get(f'https://www-old.cev.eu/Competition-Area/History.aspx?ID=1295')  # contains table with all years
        link = driver.find_element(By.PARTIAL_LINK_TEXT, f'{year}').get_attribute('href')
        driver.get(link)
        # it's not possible to use the click() function, therefore you have to get the url and use driver.get()
    except Exception as e:
        print('could not load given year!')
        print(e)
    league = f'volleyball_golden_league_men'
    get_team_standings(year, driver, league)
    get_team_stats(year, driver, league)
    get_player_stats(year, driver, league)


def get_golden_league_women(year, driver):
    try:
        driver.get(f'https://www-old.cev.eu/Competition-Area/History.aspx?ID=1296')  # contains table with all years
        link = driver.find_element(By.PARTIAL_LINK_TEXT, f'{year}').get_attribute('href')
        driver.get(link)
        # it's not possible to use the click() function, therefore you have to get the url and use driver.get()
    except Exception as e:
        print('could not load given year!')
        print(e)
    league = f'volleyball_golden_league_women'
    get_team_standings(year, driver, league)
    get_team_stats(year, driver, league)
    get_player_stats(year, driver, league)


def get_team_stats(year, driver, league):
    try:  # load data
        driver.find_element(By.PARTIAL_LINK_TEXT, f'Statistics').click()
        time.sleep(3)
        elements = driver.find_elements(By.CLASS_NAME, 'rtsTxt')
        for element in elements:
            if element.text == 'Team Stats':
                element.click()
                break
        tables = driver.find_elements(By.ID, "Content_Left_ctl00_TabInfo")
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            df = check_tables(df)
            filename = f'{league}_team_stats_{year}.csv'
            safe_csv(df, filename)
    except Exception as e:
        print('could not scrape data')
        print(e)


def get_team_standings(year, driver, league):
    try:  # load data
        driver.find_element(By.PARTIAL_LINK_TEXT, f'Home').click()
        time.sleep(3)
        tables = driver.find_elements(By.CLASS_NAME, "rgMasterTable")
        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]
            df = check_tables(df)
            filename = f'{league}_team_standings_{year}.csv'
            safe_csv(df, filename)
    except Exception as e:
        print('could not scrape data')
        print(e)


def get_player_stats(year, driver, league):
    try:  # load data
        driver.find_element(By.PARTIAL_LINK_TEXT, f'Statistics').click()
        time.sleep(3)
        select_element = driver.find_element(By.ID, 'Content_Left_DDL_PlayerRanking')
        select = Select(select_element)
        option_list = select.options
        for index in range(0, len(option_list)):
            select_element = driver.find_element(By.ID, 'Content_Left_DDL_PlayerRanking')
            select = Select(select_element)
            option_list = select.options
            name = option_list[index].accessible_name.replace(" ", "_").lower()
            select.select_by_index(index)
            tables = driver.find_elements(By.CLASS_NAME, "rgMasterTable")
            table_counter = 1
            for table in tables:
                html = table.get_attribute("outerHTML")
                df = pd.read_html(html)[0]
                df = check_tables(df)
                filename = f'{league}_{name}_{table_counter}_{year}.csv'  # problem with naming
                safe_csv(df, filename)
                table_counter = table_counter + 1
    except Exception as e:
        print('could not scrape data')
        print(e)
# %%

# %%
