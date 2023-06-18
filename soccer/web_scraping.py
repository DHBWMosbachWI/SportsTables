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
        assert len(table_header) == len(content_row), "table header should be of same length as the table body row"
        row = []
        for data_cell in content_row:
            # print(data_cell.get_text())
            row.append(data_cell.get_text().strip())
        content_data.append([data_cell.get_text().strip() for data_cell in content_row])

    df = pd.DataFrame(content_data, columns=table_header)
    return df


def get_soccer_leagues_ids():
    response = requests.get("https://fbref.com/en/comps/")
    soup = BeautifulSoup(response.content, "html.parser")
    big5_table = soup("table")[2]
    soccer_leagues = []
    for row in big5_table.find("tbody")("tr"):
        soccer_leagues.append({
            "league_name": row.find("th").get_text(),
            "league_stats_name": row("td")[-2].find("a")["href"].split("/")[-1],
            "league_id": row("td")[-2].find("a")["href"].split("/")[3]
        })

    return soccer_leagues


def get_soccer_teams_url(season: int, current_season: int, league_id: int = 20,
                         league_stats_name: str = "Bundesliga-Stats"):
    if season == current_season:
        url = f"https://fbref.com/en/comps/{league_id}/{league_stats_name}"
    else:
        url = f"https://fbref.com/en/comps/{league_id}/{season}-{season + 1}/{season}-{season + 1}-{league_stats_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    teams_url_stats = []
    for table_row in soup.findAll("table")[0].find("tbody")("tr"):
        teams_url_stats.append({table_row.find("a").contents[0]: table_row.find("a")["href"]})
    return teams_url_stats


def get_team_season_stats(season: int, current_season: int, league_id: int = 20,
                          league_stats_name: str = "Bundesliga-Stats"):
    if season == current_season:
        url = f"https://fbref.com/en/comps/{league_id}/{league_stats_name}"
    else:
        url = f"https://fbref.com/en/comps/{league_id}/{season}-{season + 1}/{season}-{season + 1}-{league_stats_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[1])
    return df


def get_player_season_stats(season, current_season, league_id,
                            league_stats_name, driver):
    teams_urls = get_soccer_teams_url(season, current_season, league_id, league_stats_name)

    tables_dict = {}
    for team_url in teams_urls:
        url = f"https://fbref.com{list(team_url.values())[0]}"
        driver.get(url)
        # print(url)
        time.sleep(5)  ## wait 5 seconds until the next request to avoid getting blocked by the website
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all('table')

        for table in tables:
            table_id = table.get('id')
            if table_id is not None:
                year = url.split('/')[-2]
                key = f'{table_id}_{year}'
                df = pd.read_html(str(table))[0]
                if key in tables_dict:
                    tables_dict[key] = pd.concat([tables_dict[key], df], ignore_index=True)
                else:
                    tables_dict[key] = df
    driver.quit()

    for key, df in tables_dict.items():
        name = f'{league_stats_name}_{key}.csv'
        df.to_csv(name, index=False)
        print(f'Saved {name}')
    return df


def get_player_season_stats2(season, current_season, league_id,
                             league_stats_name, driver, year):
    teams_urls = get_soccer_teams_url(season, current_season, league_id, league_stats_name)

    dataframes = []
    for team_url in teams_urls:
        url = f"https://fbref.com{list(team_url.values())[0]}"
        # print(url)
        time.sleep(3)  ## wait 3 seconds until the next request to avoid getting blocked by the website
        driver.get(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dataframes.append(web_table_to_dataframe(soup("table")[0]))

    df = pd.concat(dataframes, ignore_index=True)
    df = check_tables(df)
    name = f'soccer_{league_stats_name}_player_stats_{year}.csv'
    df.to_csv(name, index=False)
    print(f'Saved {name}')


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


def get_soccer_league_season_standings(league, year, driver):
    if league == 'premier_league':
        url = f'https://fbref.com/en/comps/9/{year}-{year+1}/{year}-{year+1}-Premier-League-Stats'
    elif league == 'ligue_1':
        url = f'https://fbref.com/en/comps/13/{year}-{year+1}/{year}-{year+1}-Ligue-1-Stats'
    elif league == 'serie_a':
        url = f'https://fbref.com/en/comps/11/{year}-{year+1}/{year}-{year+1}-Serie-A-Stats'
    elif league == 'la_liga':
        url = f'https://fbref.com/en/comps/12/{year}-{year+1}/{year}-{year+1}-La-Liga-Stats'
    elif league == 'fussball-bundesliga':
        url = f'https://fbref.com/en/comps/20/{year}-{year+1}/{year}-{year+1}-Bundesliga-Stats'
    elif league == 'champions-league':
        url = f'https://fbref.com/en/comps/8/{year}-{year+1}/{year}-{year+1}-Champions-League-Stats'

    driver.get(url)
    time.sleep(5)
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all('table')
        for table in tables:
            table_id = table.get('id')
            if table_id is not None:
                df = pd.read_html(str(table))[0]
                df = check_tables(df)
                name = f'soccer_{league}_{table_id}_{year}.csv'
                df.to_csv(name, index=False)
                print(f'Saved {name}')
    except Exception as e:
        print("not possible")
        print(e)
        pass

def get_soccer_league_scores(league, year, driver):
    if league == 'premier_league':
        url = f'https://fbref.com/en/comps/9/{year}-{year+1}/schedule/{year}-{year+1}-Premier-League-Scores-and-Fixtures'
    elif league == 'ligue_1':
        url = f'https://fbref.com/en/comps/13/{year}-{year+1}/schedule/{year}-{year+1}-Ligue-1-Scores-and-Fixtures'
    elif league == 'serie_a':
        url = f'https://fbref.com/en/comps/11/{year}-{year+1}/schedule/{year}-{year+1}-Serie-A-Scores-and-Fixtures'
    elif league == 'la_liga':
        url = f'https://fbref.com/en/comps/12/{year}-{year+1}/schedule/{year}-{year+1}-La-Liga-Scores-and-Fixtures'
    elif league == 'fussball-bundesliga':
        url = f'https://fbref.com/en/comps/20/{year}-{year+1}/schedule/{year}-{year+1}-Bundesliga-Scores-and-Fixtures'
    elif league == 'champions-league':
        url = f'https://fbref.com/en/comps/8/{year}-{year+1}/schedule/{year}-{year+1}-Champions-League-Scores-and-Fixtures'

    driver.get(url)
    time.sleep(5)
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all('table')
        for table in tables:
            table_id = table.get('id')
            if table_id is not None:
                df = pd.read_html(str(table))[0]
                df = check_tables(df)
                filename = f'soccer_{league}_{table_id}_{year}.csv'
                df.to_csv(filename, index=False)
                print(f'Saved {filename}')

    except Exception as e:
        print("not possible")
        print(e)
        pass

# %%

# %%
