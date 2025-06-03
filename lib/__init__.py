import sqlite3

CONN = sqlite3.connect('magazine.db')
CURSOR = CONN.cursor()
