from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
import json

def load_embeddings(file_path):
    """Load embeddings from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)

def store_embeddings_in_qdrant(embeddings, collection_name="articles", vector_size=384):
    client = QdrantClient(host="qdrant", port=6333)

    # Check if the collection exists, create it if not
    try:
        client.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        print(f"Collection '{collection_name}' not found. Creating a new one.")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance="Cosine")
        )

    # Insert embeddings
    points = [
        PointStruct(
            id=i,
            vector=embedding["embedding"],
            payload={
                "chunk": embedding.get("chunk", ""),
                "title": embedding.get("title", ""),
                "metadata": embedding.get("metadata", {})
            }
        )
        for i, embedding in enumerate(embeddings)
    ]
    client.upsert(collection_name=collection_name, points=points)
    print(f"Inserted {len(points)} embeddings into Qdrant collection '{collection_name}'.")

if __name__ == "__main__":
    embeddings_file = "featurizers/embeddings.json"
    collection_name = "articles"

    # Load embeddings
    embeddings = load_embeddings(embeddings_file)
    store_embeddings_in_qdrant(embeddings, collection_name)
