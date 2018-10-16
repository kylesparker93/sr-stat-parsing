import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import sqlite3

filename = 'nfl_teams.sqlite'
conn = sqlite3.connect(filename)
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Games;


CREATE TABLE Games (
    id                      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    week                    INTEGER,
    winner                  TEXT,
    loser                   TEXT,
    winning_score           INTEGER,
    losing_score            INTEGER

);

''')

# The URL for the teams
url = 'https://www.pro-football-reference.com/years/2018/games.htm'

# Get the html and setup BeautifulSoup
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Get the rows of the teams table
table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="games")
bods = table.find('tbody')
rows = bods.findAll('tr')

# Iterate over the rows and save each school to the database if it's a school that is still playing
for row in rows:
    if (row.find('th', {"scope":"row"}) != None):
        week = int(row.find("th",{"data-stat": "week_num"}).text)
        if (week > 6):
            break
        winner = row.find("td",{"data-stat": "winner"}).text
        loser = row.find("td",{"data-stat": "loser"}).text
        pts_win = row.find("td",{"data-stat": "pts_win"}).text
        pts_lose = row.find("td",{"data-stat": "pts_lose"}).text
        print(week, winner, loser, pts_win, pts_lose, sep='    ')
        cur.execute('''INSERT OR IGNORE INTO Games (week, winner, loser, winning_score, losing_score)
                VALUES (?, ?, ?, ?, ?)''', (week, winner, loser, pts_win, pts_lose) )
        conn.commit()
