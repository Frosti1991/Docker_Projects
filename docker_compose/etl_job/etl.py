import pymongo
from sqlalchemy import create_engine
import time
from twitter_credentials import *
from etl_functions import *
import psycopg2

# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017)

# Select the database you want to use withing the MongoDB server
db = client.twitter
tweets_gasumlage=db.tweets_gasumlage
tweets_mahlzeit=db.tweets_mahlzeit

time.sleep(5)  # seconds

############ ETL - START ############

#1. Extract
extracted_tweets_gasumlage = list(tweets_gasumlage.find()) #returns list of extracted dict (original tweets and metadata)
extracted_tweets_mahlzeit = list(tweets_mahlzeit.find()) #returns list of extracted dict (original tweets and metadata)


#2. Transform
transformed_tweets_gasumlage=transform(extracted_tweets_gasumlage) #Returns list of transformed dict (scores, regex)
transformed_tweets_mahlzeit=transform(extracted_tweets_mahlzeit) #Returns list of transformed dict (scores, regex)

#3. Load

#Establish connection to postgresql
pg = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@docker_compose_prod_postgresdb_1:5432/{POSTGRES_DB}', echo=True)
#print("success")

#drop old entries
pg.execute('''
    DROP TABLE IF EXISTS tweets_gasumlage;
    ''')
pg.execute('''
    DROP TABLE IF EXISTS tweets_mahlzeit;
    ''')

#Create table in postgresdb
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets_gasumlage (
    text VARCHAR(500),
    author VARCHAR(30),
    datum TIMESTAMP,
    sentiment_score NUMERIC
);
''')
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets_mahlzeit(
    text VARCHAR(500),
    author VARCHAR(30),
    datum TIMESTAMP,
    sentiment_score NUMERIC
);
''')

#Write Tweets into table in Postgresdb
for tweet in transformed_tweets_gasumlage:
    text = tweet['text']
    author = tweet['author_id']
    date = tweet['created_at']
    score = tweet['compound']
    query = "INSERT INTO tweets_gasumlage VALUES (%s,%s,%s,%s);"
    print(text,author,date,score)
    pg.execute(query, (text, author, date, score))

for tweet in transformed_tweets_mahlzeit:
    text = tweet['text']
    author = tweet['author_id']
    date = tweet['created_at']
    score = tweet['compound']
    query = "INSERT INTO tweets_mahlzeit VALUES (%s,%s,%s,%s);"
    print(text,author,date,score)
    pg.execute(query, (text, author, date, score))

############ ETL -FINISH ##############