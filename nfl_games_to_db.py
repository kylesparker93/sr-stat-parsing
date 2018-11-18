import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from bs4 import Comment
import sqlite3

filename = 'nfl_teams.sqlite'
conn = sqlite3.connect(filename)
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Games;


CREATE TABLE Games (
    id                              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    week                            INTEGER,
    winner                          TEXT,
    winning_team_home               INTEGER,
    winning_score                   INTEGER,
    winning_team_sacks              INTEGER,
    winning_team_fumbles_forced     INTEGER,
    winning_team_fumbles_recovered  INTEGER,
    winning_team_interceptions      INTEGER,
    loser                           TEXT,
    losing_team_home,               INTEGER,
    losing_score                    INTEGER,
    losing_team_sacks               INTEGER,
    losing_team_fumbles_forced      INTEGER,
    losing_team_fumbles_recovered   INTEGER,
    losing_team_interceptions       INTEGER

);

''')

# The URL for the teams
site = 'https://www.pro-football-reference.com'
games_url = site + '/years/2018/games.htm'

# Get the html and setup BeautifulSoup
html = urllib.request.urlopen(games_url).read()
soup = BeautifulSoup(html, 'html.parser')

# Get the rows of the teams table
table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="games")
bods = table.find('tbody')
rows = bods.findAll('tr')

# Iterate over the rows and save each game
for row in rows:
    if (row.find('th', {"scope":"row"}) != None):
        week = int(row.find("th",{"data-stat": "week_num"}).text)
        if (week > 10):
            break

        # Get the winner and loser and their scores
        winner = row.find("td",{"data-stat": "winner"}).text
        loser = row.find("td",{"data-stat": "loser"}).text
        pts_win = row.find("td",{"data-stat": "pts_win"}).text
        pts_lose = row.find("td",{"data-stat": "pts_lose"}).text

        # Figure out which team was home and away so we can get the per-game stats later
        game_location = row.find("td",{"data-stat": "game_location"}).text
        if (game_location == ''):
            winning_team_home = True
            losing_team_home = False
            loc_stat_winner = 'home_stat'
            loc_stat_loser = 'vis_stat'
        else:
            winning_team_home = False
            losing_team_home = True
            loc_stat_winner = 'vis_stat'
            loc_stat_loser = 'home_stat'

        # Get the stats from the box score
        boxscore_link = row.find("td",{"data-stat": "boxscore_word"}).find('a').get('href')
        boxscore_url = site + boxscore_link
        boxscore_html = urllib.request.urlopen(boxscore_url).read()
        boxscore_soup = BeautifulSoup(boxscore_html, 'html.parser')
        all_team_stats = boxscore_soup.find("div", {"id": "all_team_stats"})

        # Maybe there's an easier way to do this, but for now it gets me the table HTML
        for comments in all_team_stats.findAll(text=lambda text:isinstance(text, Comment)):
            comments.extract()
            comment_soup = BeautifulSoup(comments, 'html.parser')
        team_stats = comment_soup.find("table", {"id": "team_stats"})
        stat_rows = team_stats.findAll("tr")

        # Iterate over the table rows to find fumbles and turnovers
        for stat_row in stat_rows:
            if (stat_row.find('th').text == "Sacked-Yards"):
                winner_sacks = stat_row.find("td", {"data-stat": loc_stat_winner}).text.split("-")[0]
                loser_sacks = stat_row.find("td", {"data-stat": loc_stat_loser}).text.split("-")[0]
                
            if (stat_row.find('th').text == "Fumbles-Lost"):
                winner_fumbles_forced = stat_row.find("td", {"data-stat": loc_stat_winner}).text.split("-")[0]
                winner_fumbles_recovered = stat_row.find("td", {"data-stat": loc_stat_winner}).text.split("-")[1]
                loser_fumbles_forced = stat_row.find("td", {"data-stat": loc_stat_loser}).text.split("-")[0]
                loser_fumbles_recovered = stat_row.find("td", {"data-stat": loc_stat_loser}).text.split("-")[1]

            if (stat_row.find('th').text == "Turnovers"):
                winner_interceptions = int(stat_row.find("td", {"data-stat": loc_stat_winner}).text) - int(winner_fumbles_recovered)
                loser_interceptions = int(stat_row.find("td", {"data-stat": loc_stat_loser}).text) - int(loser_fumbles_recovered)
        
        print(week, winner, pts_win, winning_team_home, winner_sacks, winner_fumbles_forced, winner_fumbles_recovered, winner_interceptions,
              loser, pts_lose, losing_team_home, loser_sacks, loser_fumbles_forced, loser_fumbles_recovered, loser_interceptions, sep='    ')
        cur.execute('''INSERT OR IGNORE INTO Games (week,
                winner, winning_team_home, winning_score, winning_team_sacks, winning_team_fumbles_forced, winning_team_fumbles_recovered, winning_team_interceptions,
                loser, losing_team_home, losing_score, losing_team_sacks, losing_team_fumbles_forced, losing_team_fumbles_recovered, losing_team_interceptions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (week,
                winner, winning_team_home, pts_win, winner_sacks, winner_fumbles_forced, winner_fumbles_recovered, winner_interceptions,
                loser, losing_team_home, pts_lose, loser_sacks, loser_fumbles_forced, loser_fumbles_recovered, loser_interceptions) )
        conn.commit()
