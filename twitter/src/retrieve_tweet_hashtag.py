
import datetime
import tweepy
from src.config import create_api
from src.MongoDB import returnDatabase

db = returnDatabase()
myTable = db["retrieve-trend-{}".format(datetime.date.today())]
tweets = db['trending-tweets-{}'.format(datetime.date.today())]

def retrieve_tweet():
    api = create_api()
    tags = myTable.find({}, {'tag' : 1})

    for tag in tags:
        hashtags = tag['tag']
        _dict = {}
        i = 0
        for tweet in tweepy.Cursor(api.search,q = hashtags, count = 15, result_type = 'popular').items():
            #print(tweet)
            if (i > 15):
                continue
            _dict['tweeted_at'] = tweet.created_at
            _dict['tweet'] = tweet.text
            _dict['tag'] = tag
            _dict['user'] = tweet.user.screen_name
            _dict['id'] = tweet.user.id
            #print(i)
            i += 1
            #print (tweet.created_at, tweet.text)
            tweets.find_one_and_update({'tweet' : tweet.text}, {"$set" :_dict}, upsert = True)
            
