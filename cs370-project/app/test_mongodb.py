from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017")
print("MongoDB Databases:", client.list_database_names())
