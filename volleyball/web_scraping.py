from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re


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
            # are headers repeated as rows? Remove these
    else:
        if result.columns.nlevels > 1:
            n_level = result.columns.nlevels - 1
            for index in range(n_level):
                result.columns = result.columns.droplevel(0)  # drop first layer
        columns = list(result.columns)
        new_result = result.loc[result[columns[0]] != columns[0]]
    return new_result


def get_volleyball_league_scores(year, driver):
    url = f'https://www.volleyball-bundesliga.de/cms/home/1_bundesliga_maenner/archiv/statistikrankings/saison_{year}_{year + 1 - 2000}.xhtml'
    driver.get(url)
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")

        for table in tables:
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html)[0]

    except Exception as e:
        print("not possible")
        print(e)
        pass
    return df


def get_volleyball_league_scores_bundesliga_men(year, driver):
    url = f'https://www.volleyball-bundesliga.de/cms/home/1_bundesliga_maenner/archiv/statistikrankings/saison_{year}_{year + 1 - 2000}.xhtml'
    driver.get(url)
    time.sleep(5)
    try:
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
    try:
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

#%%
