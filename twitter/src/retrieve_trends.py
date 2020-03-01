
import tweepy
import logging
import geocoder
from src.postgres import myConnection
from src.MongoDB import returnDatabase

from src.config import create_api
import datetime

api = create_api()
db = returnDatabase()

myTable = db["retrieve-trend-{}".format(datetime.date.today())]
print(myTable)


def prettify(func):
    def wrapper():
        _ = func()
        _ = _[0]['trends']
        f = open('trending.csv', 'w', encoding="utf-8")
        xstr = lambda s: str(s) or ""

        for t in _:
            f.write(xstr(t['name'])+ ',')
            f.write(xstr(t['url']) + ',')
            f.write(xstr(t['query']) + ',')
            f.write(xstr(t['tweet_volume']))
            f.write('\n')

        f.close()
    return wrapper

# def prettifyDB(func):
#     def wrapper():
#         _ = func()
#         print('a')
#         _ = _[0]['trends']
#         f = open('trending.csv', 'w', encoding="utf-8")
#         xstr = lambda s: str(s) or ""
#         i = 0
#         for t in _:
#             _dict = {}
#             _dict['name'] = xstr(t['name'])
#             _dict['url'] = xstr(t['url'])
#             _dict['tag'] = xstr(t['query'])
#             _dict['tweet_count'] = xstr(t['tweet_volume'])
#             _dict['time_stamp'] = datetime.datetime.now()
#             i += 1
#             if i >= 10:
#                 break

#             #print(myTable.find(my_query))
#             # myTable.update({'url' : _dict['url']}, _dict, upsert=False)
#             myTable.insert_one(_dict)
#             #myTable.find_one_and_update({'url' : xstr(t['url'])},
#             #                            {'$set' : {'tweet_count' : xstr(t['tweet_volume'])}})
    
#     print("Done")
#     return wrapper



def location():
    g = geocoder.ip('me')
    return g.latlng

def get_woeid():
    lat, long = location()
    return api.trends_closest(lat, long)[0]['woeid']

@prettify
def get_trends():
    woeid = get_woeid()
    return api.trends_place(woeid)

# @prettifyDB
def get_trends_db():
    # woeid = get_woeid()
    # print(woeid)
    _ =  api.trends_place(2282863)
    
    _ = _[0]['trends']
    # print(_)
    f = open('trending.csv', 'w', encoding="utf-8")
    xstr = lambda s: str(s) or ""
    i = 0
    updates = []
    for t in _:
        _dict = {}
        _dict['name'] = xstr(t['name'])
        _dict['url'] = xstr(t['url'])
        _dict['tag'] = xstr(t['query'])
        _dict['tweet_count'] = xstr(t['tweet_volume'])
        _dict['time_stamp'] = datetime.datetime.now()
        i += 1
        if i >= 10:
            break
        updates.append(_dict)

        #print(myTable.find(my_query))
        print(_dict)
    # myTable.insert_many(updates)
    
        myTable.find_one_and_update({'tag' : _dict['tag']}, {"$set" : _dict}, upsert=True)
        #myTable.find_one_and_update({'url' : xstr(t['url'])},
        #                            {'$set' : {'tweet_count' : xstr(t['tweet_volume'])}})

    print("Done")





