import sqlite3

conn = sqlite3.connect('ItalyTweets.db')
c = conn.cursor()
symbol = 'italy'
rows = c.execute("select count(hashtags) from tweets where hashtags like ?",('%'+symbol+'%',))
rows = c.execute("select count(hashtags) from tweets where hashtags like ?",('%'+symbol+'%',))

for row in rows:
    print(row)
conn.close()