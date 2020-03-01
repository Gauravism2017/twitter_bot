
import tweepy
import logging
import csv
import re

from src.config import create_api
from src.MongoDB import returnDatabase

db = returnDatabase()

def clean_tag_id(tweet):

    user_mentions_id = []
    user_mentions_name = []
    for _ in tweet.entities['user_mentions']:
        user_mentions_id.append(_['id'])
    return user_mentions_id

def clean_tag_name(tweet):
    user_mentions_name = []
    for _ in tweet.entities['user_mentions']:
        user_mentions_name.append(_['screen_name'])
    return user_mentions_name



def get_tweets(username):
    api = create_api()
    number_tweets = 20000
    tweets = api.user_timeline(screen_name = username)
    #tmp = []
    #print(tweets)

    tweet_list = [[tweet.text, tweet.created_at, clean_tag_id(tweet), clean_tag_name(tweet)]
                for tweet in tweets]
    # print(tweet_csv)
    #tweet_list = []
    #for _ in tweet_csv:
    #    single_tweet = []
    #    tagged = []
    #    for t in _.split(" "):
    #        if '@' in t:
    #            tagged.append(t)
    #            _ = _.replace(t, "")
    #    single_tweet.append(tagged)
    #    single_tweet.append(_)
    #    tweet_list.append(single_tweet)

    ##print(tweet_list)
    myTable = db['tweets']
    for _ in tweet_list:
        _dict = {}
        _dict['tweet'] = _[0]
        _dict['timestamp'] = _[1]
        _dict['id_mentioned'] = _[2]
        _dict['name_mentioned'] = _[3]
        myTable.update({'timestamp' : _dict['timestamp']}, _dict, upsert = True)
    ##with open("tweetsby{}.csv".format(username), 'w'):
    ##    for _ in tweet_list:
    ##        for __ in _[0]:
    ##            file.write(__)
    ##            file.write(" ")
    ##        file.write(", ")
    ##        file.write(_[1] + "\n")





if __name__ == "__main__":
    get_tweets("@Gauravism_2017")