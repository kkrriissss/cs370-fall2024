from pymongo import MongoClient

def fetch_articles_from_mongo(uri="mongodb://mongodb:27017/", db_name="rag_database", collection="articles"):
    client = MongoClient(uri)
    db = client[db_name]
    articles = list(db[collection].find())
    return articles


def tokenize_content(content, max_length=512):

    words = content.split()
    return [" ".join(words[i:i + max_length]) for i in range(0, len(words), max_length)]


def preprocess_articles(articles, max_length=512):
    preprocessed_data = []
    for article in articles:
        content = article.get("content", "")
        metadata = article.get("metadata", {})
        title = article.get("title", "No Title")

        # Tokenize content into smaller chunks
        chunks = tokenize_content(content, max_length)

        # Add each chunk to preprocessed data
        for chunk in chunks:
            preprocessed_data.append({
                "title": title,
                "chunk": chunk,
                "metadata": metadata
            })
    return preprocessed_data


def save_preprocessed_data(data, file_path):
    import json
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Preprocessed data saved to {file_path}")


if __name__ == "__main__":
    db_uri = "mongodb://mongodb:27017/"
    db_name = "rag_database"
    collection_name = "articles"
    output_file = "featurizers/preprocessed_data.json"

    articles = fetch_articles_from_mongo(db_uri, db_name, collection_name)
    preprocessed_data = preprocess_articles(articles)
    save_preprocessed_data(preprocessed_data, output_file)

