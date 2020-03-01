
import pymongo

def returnDatabase(db_name = 'twitter'):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    try:
        db = client[db_name]
    except:
        print("Connect failed")
    return db