

import tweepy
import logging
from src.config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api):
    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"following {follower.name}")
            follower.follow()
    print("Done")


def main():
    api = create_api()
    a = 1
    while a:
        follow_followers(api)
        logger.info("waiting")
        a += 1
        if (a == 5):
            a = 0

if __name__ == "__main__":
    main()