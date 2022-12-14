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
            #print(data_cell.get_text())
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
            "league_name":row.find("th").get_text(),
            "league_stats_name": row("td")[-2].find("a")["href"].split("/")[-1], 
            "league_id":row("td")[-2].find("a")["href"].split("/")[3]
            })
        
    return soccer_leagues
    

def get_soccer_teams_url(season:int, current_season:int, league_id:int=20, league_stats_name:str="Bundesliga-Stats"):
    if season == current_season:
        url = f"https://fbref.com/en/comps/{league_id}/{league_stats_name}"
    else:
        url = f"https://fbref.com/en/comps/{league_id}/{season}-{season+1}/{season}-{season+1}-{league_stats_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    teams_url_stats = []
    for table_row in soup.findAll("table")[0].find("tbody")("tr"):
        teams_url_stats.append({table_row.find("a").contents[0]:table_row.find("a")["href"]})
    return teams_url_stats


def get_player_season_stats(season:int, current_season:int, league_id:int=20, league_stats_name:str="Bundesliga-Stats"):
    teams_urls = get_soccer_teams_url(season, current_season, league_id, league_stats_name)

    dataframes = []
    for team_url in teams_urls:
        url = f"https://fbref.com{list(team_url.values())[0]}"
        #print(url)
        time.sleep(3) ## wait 3 seconds until the next request to avoid getting blocked by the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dataframes.append(web_table_to_dataframe(soup("table")[0]))
        
    df = pd.concat(dataframes, ignore_index=True)
    return df

def get_team_season_stats(season:int, current_season:int, league_id:int=20, league_stats_name:str="Bundesliga-Stats" ):
    if season == current_season:
        url = f"https://fbref.com/en/comps/{league_id}/{league_stats_name}"
    else:
        url = f"https://fbref.com/en/comps/{league_id}/{season}-{season+1}/{season}-{season+1}-{league_stats_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[1])
    return df
        


### get regular season table
def get_soccer_league_season_standings(season:int, current_season:int, league_id:int=20, league_stats_name:str="Bundesliga-Stats"):
    if season == current_season:
        url = f"https://fbref.com/en/comps/{league_id}/{league_stats_name}"
    else:
        url = f"https://fbref.com/en/comps/{league_id}/{season}-{season+1}/{season}-{season+1}-{league_stats_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    df = web_table_to_dataframe(soup("table")[0])
    return df