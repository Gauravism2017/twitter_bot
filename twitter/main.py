
import src.follow as follow
import src.retrieve_tweet_user as retrieve
import src.retrieve_trends as trends
from src.retrieve_tweet_hashtag import retrieve_tweet
from src.get_tagged_tweets import tagged_tweets

def tweet_collect():
    follow.main()
    retrieve.get_tweets('Gauravism_2017')
    # trends.location()
    trends.get_trends_db()
    retrieve_tweet()
    tagged_tweets()






