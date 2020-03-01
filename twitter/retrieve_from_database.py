from src.MongoDB import returnDatabase
from src.config import create_api
import pprint
from bot.cleaning.config import save_dir
import re
import os
from bson.objectid import ObjectId


db = returnDatabase()

myTable = db["mentions"]

file = open(os.path.join(save_dir,"inp.txt"), 'w', encoding="utf-8")
tags = open(os.path.join(save_dir,"tags.txt"), 'w', encoding="utf-8")
id = open(os.path.join(save_dir,"id.txt"), 'w', encoding="utf-8") 
db_id = open(os.path.join(save_dir,"db.txt"), 'w', encoding="utf-8") 

for _ in myTable.find({'replied' : 0}):
    if (1):
        string = re.sub(r'([^\s\w.,!]|_)+', '', _["tweet"])
        string = re.sub(r'[^0-9a-zA-Z]+', ' ', string)
        #string.replace(".", " ")
        string = ' '.join(string.split())
        print(string , file = file)
        #print("--reset" , file = file)
        print(_["tweeted_by"], file = tags)
        print(_["tweeted_id"], file = id)
        print(_["_id"], file = db_id)
    #_["replied"] = 1
    #myTable.update_one({"_id" : _["_id"]}, _, upsert = True)
        

file.close()
tags.close()
id.close()