import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

# The URL for the schools
url = 'https://www.sports-reference.com/cfb/schools/'

# Get the html and setup BeautifulSoup
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Get the rows of the schools table
table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="schools")
bods = table.find('tbody')
rows = bods.findAll('tr')

# Iterate over the rows and save each school to the database if it's a school that is still playing
for row in rows:
  if (row.find('th', {"scope":"row"}) != None):
    year = row.find("td",{"data-stat": "year_max"}).text
    if (year == '2018'):
      team = row.find("td",{"data-stat": "school_name"}).text
        print(team) # TODO
