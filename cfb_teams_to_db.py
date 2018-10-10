import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import sqlite3

filename = 'cfb_teams.sqlite'
conn = sqlite3.connect(filename)
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Teams;


CREATE TABLE Teams (
    id                      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    team                    TEXT UNIQUE,
    rating                  INTEGER,
    week_one_rating         INTEGER,
    week_two_rating         INTEGER,
    week_three_rating       INTEGER,
    week_four_rating        INTEGER,
    week_five_rating        INTEGER,
    week_six_rating         INTEGER,
    week_seven_rating       INTEGER,
    week_eight_rating       INTEGER,
    week_nine_rating        INTEGER,
    week_ten_rating         INTEGER,
    week_eleven_rating      INTEGER,
    week_twelve_rating      INTEGER,
    week_thirteen_rating    INTEGER,
    week_fourteen_rating    INTEGER,
    week_fifteen_rating     INTEGER,
    week_sixteen_rating     INTEGER

);

''')

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
            print(team)
            cur.execute('''INSERT OR IGNORE INTO Teams (team)
                VALUES ( ? )''', (team, ) )
            conn.commit()
