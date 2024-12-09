from pymongo import MongoClient
import json


def connect_to_mongo(uri="mongodb://mongodb:27017/", db_name="rag_database"):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        print(f"Connected to MongoDB database: {db_name}")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def load_data_to_mongo(db, collection_name, data):
    try:
        collection = db[collection_name]
        result = collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} documents into collection '{collection_name}'.")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")


if __name__ == "__main__":
    transformed_file = "extractors/transformed_articles.json"
    collection_name = "articles"

    try:
        with open(transformed_file, "r") as f:
            transformed_data = json.load(f)
    except Exception as e:
        print(f"Error loading transformed data: {e}")
        transformed_data = []

    db = connect_to_mongo()

    if db is not None:
        load_data_to_mongo(db, collection_name, transformed_data)
    else:
        print("Failed to connect to MongoDB. Data not loaded.")
