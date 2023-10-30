import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/wba_4_11h")
print(f"Databases: {client.list_database_names()}")
db = client.get_database('wab_4_11h')
print(f"{db.name} collections: {db.list_collection_names()}")
collection = db.get_collection('rabbit')
print(f"Open {collection.name}")
