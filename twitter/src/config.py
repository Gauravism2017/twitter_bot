

import tweepy
import logging
import src.api_keys as keys


logger = logging.getLogger()

def create_api():
    consumer_key = keys.CONSUMER_KEY
    consumer_Secret = keys.CONSUMER_SECRET
    access_token= keys.ACCESS_TOKEN
    access_token_secret = keys.ACCESS_TOKEN_SECRET


    auth = tweepy.OAuthHandler(consumer_key, consumer_Secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e

    logger.info("API Created")
    return api
