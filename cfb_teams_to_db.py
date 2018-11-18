import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import sqlite3

filename = 'cfb_data.sqlite'
conn = sqlite3.connect(filename)
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Teams;


CREATE TABLE Teams (
    id                      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    team                    TEXT,
    rating                  INTEGER,
    wins                    INTEGER,
    losses                  INTEGER,
    ties                    INTEGER,
    preseason_rating,       INTEGER,
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
