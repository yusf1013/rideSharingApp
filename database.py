# just type mongo in command prompt
from pymongo import MongoClient
from bson import json_util
import json


def insert_into_database(database, collection, document):
    client = MongoClient('localhost')
    db = client[database]
    col = db[collection]

    result = col.insert_one(document)


def update_database(database, collection, document, new_data):
    client = MongoClient('localhost')
    db = client[database]
    col = db[collection]

    result = col.update_one(document, {'$set' : new_data})


def find_from_database(database, collection, document):
    client = MongoClient('localhost')
    db = client[database]
    col = db[collection]

    result = col.find_one(document)
    # return json.dumps(result, indent=4, default=json_util.default)
    return result


def insert_or_update_db(database, collection, document, id_key):
    find_doc = {id_key: document[id_key]}
    result = find_from_database(database, collection, find_doc)
    if result is None or str(result) == "null":
        insert_into_database(database, collection, document)
    else:
        update_database(database, collection, find_doc, document)


# r = update_database("test_database", "test", {"author": "Yusuf Bro", "price":100}, {"author": "Yusuf Ahmed"})
# print(r)
