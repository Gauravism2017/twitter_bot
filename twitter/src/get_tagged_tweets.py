import datetime
import tweepy
from src.config import create_api
from src.MongoDB import returnDatabase
import pprint
from bson.objectid import ObjectId


db = returnDatabase()
mention = db['mentions']

def clean(text):
    for t in text.split(" "):
            if '@' in t:
                #tagged.append(t)
                text = text.replace(t, "")
    return text

def alreadyExists(newID):
    #print(newID)
    if(mention.count_documents({'tweeted_id': str(newID)}, limit = 1) != 0):
        return True
    else:
        return False

def tagged_tweets():
    api = create_api()
    for mentions in tweepy.Cursor(api.mentions_timeline).items():
        if(alreadyExists(mentions.id)):
            #print(mentions.id)
            continue
        else:
            _dict = {}
            _dict['tweet'] = clean(mentions.text)
            _dict['tweeted_by'] = str(mentions.user.screen_name)
            _dict['tweeted_id'] = str(mentions.id)
            _dict['timestamp'] = mentions.created_at
            _dict['replied'] = 1
            #pprint.pprint(_dict)
            mention.find_one_and_update({'tweeted_id' : _dict['tweeted_id']}, {"$set": _dict}, upsert = True)
            #mention.insert(_dict)
        #print(mentions)
