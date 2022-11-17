from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
response = session.get(
    "https://www.baseball-reference.com/leagues/majors/2022-standard-batting.shtml")
response.html.render()

# soup = BeautifulSoup(r.html.raw_html, "html.parser")
# print(len(soup("table")))