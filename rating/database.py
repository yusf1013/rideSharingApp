# just type mongo in command prompt
from pymongo import MongoClient

conn_name = 'database'
conn_port = 27017


def insert_into_database(database, collection, document):
    client = MongoClient(conn_name, conn_port)
    # client = MongoClient()
    db = client[database]
    col = db[collection]

    result = col.insert_one(document)
    print("Insert successful")


def update_database(database, collection, document, new_data):
    client = MongoClient(conn_name, conn_port)
    db = client[database]
    col = db[collection]

    result = col.update_one(document, {'$set': new_data})
    print("Update success")


def find_from_database(database, collection, document):
    client = MongoClient(conn_name, conn_port)
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

# if __name__ == "__main__":
#     shit = {"Life is": "SHIT"}
#     insert_into_database("ride_sharing_app", "ratings", shit)
