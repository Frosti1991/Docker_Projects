import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def regex(tweet):
    url_pattern="(https:\/\/t.co\/([a-zA-Z0-9_]+))"
    at_pattern="(@([a-zA-Z0-9_]+))"
    hashtag_pattern="(#([a-zA-Z0-9_]+))"
    rt_pattern="RT : "
    
    tweet_new =re.sub(url_pattern, '', tweet)
    tweet_new=re.sub(at_pattern, '', tweet_new)
    tweet_new=re.sub(hashtag_pattern, '', tweet_new)
    tweet_new=re.sub(rt_pattern, '', tweet_new)
    
    return tweet_new 

def sentiment_score(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores   

def transform(extracted_tweets):
    '''Transforms the data'''
    transformed_tweets = []
    for dict_tweet in extracted_tweets:
        dict_tweet_postgres={}
        # 1. regex (return is a string)
        tweet_new=regex(dict_tweet['text'])
        dict_tweet['text']=tweet_new
        
        # 2. sentiment
        dict_score=sentiment_score(tweet_new)
        
        #3. combine dict_sccore and dict_tweet
        dict_tweet_postgres= {**dict_tweet, **dict_score}
        
        #4. append to list of dictionaries
        transformed_tweets.append(dict_tweet_postgres)
        # transformed_tweets is a list of transformed dictionaries
    return transformed_tweets