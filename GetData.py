import os
import sys
import string
import time
from twython import Twython
import sqlite3

consumer_key='QS0rA884dYiScP28uLMPey8YE'
consumer_secret='WeAZkWLR2iTuBht4qSjz6cxBsAyCTQrAhoiQMyNKACSOimdU9e'
access_token_key='709478557978796033-6Ws1xpLMSsqnPkdzbnNTcCGLwtAOagM'
access_token_secret='OjjWKG3cQvTaPqaNVwClzFFbBOU7fxkiJM6WBnLLR4XLP'
MAX_ATTEMPTS = 1000

def insert(conn, id, date, text, lang, place, retweetCount, favoriteCount,hashtags,lat, long, url):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tweets VALUES (?,?,?,?,?,?,?,?,?,?,?);
        ''', (id, date, text, lang, place, retweetCount, favoriteCount,hashtags,lat, long, url))
    conn.commit()

# Create the database if it doesn't exist
def createDB():
    if not os.path.exists('ItalyTweets.db'):
        conn = sqlite3.connect('ItalyTweets.db')
        conn.close()
        print("Successfully created DB")
    else:
        pass

# Create the table if it's not in the db
def createTable():
    conn = sqlite3.connect('ItalyTweets.db')
    print("Checking if table exists, else create table")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tweets
        (id Text, date Date, text Text, lang Text, place Text, retweetCount Integer, favoriteCount Integer, hashtags Text , lat Float, long Float, url Text )
        ''')
    conn.commit()
    conn.close()

def getTweets():

    twitter = Twython(consumer_key, consumer_secret,access_token_key,access_token_secret)
    twitter.verify_credentials()

    tweets = 0
    # get sqlite3 connection
    conn = sqlite3.connect('ItalyTweets.db')
    next_max_id = 708934749390311423;
  #results = twitter.cursor(twitter.search, q='#italy',count = 5000,   #**supply whatever query you want here**
        #                  since='2016-03-01')

    for i in range(1,MAX_ATTEMPTS):

        if(tweets == 5000):
            time.sleep(120)
            tweets = 0
        try:
            if(0 == i):
                results    = twitter.search(q="italy",count='100',since='2016-03-01')
            else:
                results    = twitter.search(q="italy",include_entities='true',max_id=next_max_id,since='2016-03-01',count='100')

        except:
            print("Rate limit reached, taking a break for a minute...\n")
            time.sleep(60)

        # Store tweets
        for result in results['statuses']:
            tweets = tweets + 1
            hashtags = ""
            for hashtag in result['entities']['hashtags']:
                hashtags += hashtag["text"] + ","

            urls = ""
            for url in result['entities']['urls']:
                urls += url["url"] + ","

            lat = ""
            long = ""
            if result['coordinates'] is not None:
                lat = result['coordinates']['coordinates'][0]
                long = result['coordinates']['coordinates'][1]

            place = ""
            if result['place'] is not None:
                place = result['place']['name']
            insert(conn, result['id'], result['created_at'], result['text'], result['lang'], place, result['retweet_count'], result['favorite_count'] ,hashtags,lat, long, urls)


        # Parse the data returned to get max_id to be passed in consequent call.
        #print(results['search_metadata'])
        print(tweets)

        try:
            next_results_url_params  = results['search_metadata']['next_results']
            next_max_id  = next_results_url_params.split('max_id=')[1].split('&')[0]
            print("Next id: " + str(next_max_id))
        except:
            print("Max id not present")
            next_max_id = result['id'] - 1
            print("Next id: " + str(next_max_id))

    conn.close()

createDB()
createTable()
getTweets()