import os
from src.config import create_api
from src.MongoDB import returnDatabase
from bot.cleaning.config import save_dir
from bson.objectid import ObjectId


db = returnDatabase()
myTable = db["mentions"]

file = open(os.path.join(save_dir,"out.txt"), 'r', encoding="utf-8")
tags = open(os.path.join(save_dir,"tags.txt"), 'r', encoding="utf-8")
ids = open(os.path.join(save_dir,"id.txt"), 'r', encoding="utf-8")
db_ids = open(os.path.join(save_dir,"db.txt"), 'r', encoding="utf-8") 

api = create_api()

status = [x.strip() for x in file.readlines()] 
status = [x for x in status if x] 
db_id = [x.strip() for x in db_ids.readlines()] 
tag = [x.strip() for x in tags.readlines()] 
id = [x.strip() for x in ids.readlines()]

#print(status)
count = 0
print("len of status : {}\n len of db_id : {}\n len of tags : {}\n len of id : {}".
      format(len(status), len(db_id), len(tag), len(id)))
for t, i, s, d in zip(tag, id, status, db_id):
    myTable.update_one({"_id": ObjectId(d)},
                   {'$set': {"replied": 1
                             }
                    },
                    upsert=True)
    # api.update_status(status = "@Gauravism_2017 " + s + " @" + t, in_reply_to_status_id = i)
    # count = count + 1
    try:
        api.update_status(status = "@Gauravism_2017 " + s + " @" + t, in_reply_to_status_id = i)
        count = count + 1
    except ValueError:
    	print(s+'\n')
    	print('ValueError')
    except ImportError:
    	print(s+'\n')
    	print('ImportError')
    except EOFError:
    	print(s+'\n')
    	print('EOFError')

    except Exception as e:
        print(s+'\n')
        print(e)

print(count)
    

