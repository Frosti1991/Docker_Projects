#Loading Scripts and Libraries
from twitter_credentials import *
import tweepy
import logging
import pymongo

# Authentification
client=tweepy.Client(bearer_token=Bearer_Token,
                    access_token=API_Key,
                    access_token_secret=API_Key_Secret)

if client: #checks if is "not None"
    logging.critical("\nAuthentication nice")
else:
    logging.critical("\nCredentials invalid!")

# Define a search string

query1="Gasumlage -is:retweet"
query2="Mahlzeit"

#look for this search string
search_gasumlage=client.search_recent_tweets(query=query1, tweet_fields=['id','created_at','text','conversation_id','referenced_tweets','author_id'],max_results=50)
search_mahlzeit=client.search_recent_tweets(query=query2, tweet_fields=['id','created_at','text','conversation_id','referenced_tweets','author_id'],max_results=50)

#Connect to MongoDB
client = pymongo.MongoClient(host="mongodb", port=27017)

#Empty MongoDB
client.drop_database('twitter')

#Instanciate new DB 'twitter'
db = client.twitter

#Create result and table list
result_list=[search_gasumlage,search_mahlzeit]
table_list=["tweets_gasumlage","tweets_mahlzeit"]

for result in result_list:
    for tweet in result.data:
        logging.critical(f'\n\n\nINCOMING TWEET:\n{tweet.text}\n\n{tweet.created_at}\n')
        index=result_list.index(result)
        table_name=table_list[index]
        #print(index)
        db[table_name].insert_one(dict(tweet))
