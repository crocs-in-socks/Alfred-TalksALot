import requests
from bs4 import BeautifulSoup

goog_search = "https://www.google.com/search?client=firefox-b-d&q=hello+there"

r = requests.get(goog_search)

soup = BeautifulSoup(r.text, "html.parser")
brief = soup.find_all()
print(brief)