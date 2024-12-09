from sentence_transformers import SentenceTransformer
import json


def generate_embeddings(data, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = []

    for item in data:
        embedding = model.encode(item["chunk"])
        embeddings.append({
            "embedding": embedding.tolist(),
            "chunk": item["chunk"],  # Add the chunk text
            "title": item["title"],  # Add the title
            "metadata": item["metadata"]  # Add the metadata
        })

    return embeddings


def save_embeddings(data, output_file):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    input_file = "featurizers/preprocessed_data.json"
    output_file = "featurizers/embeddings.json"

    # Load preprocessed data
    with open(input_file, "r") as f:
        preprocessed_data = json.load(f)
    embeddings = generate_embeddings(preprocessed_data)
    save_embeddings(embeddings, output_file)

    print(f"Embeddings saved to {output_file}")
