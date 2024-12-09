from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import requests

OLLAMA_API_URL = "http://ollama:54321/api/generate"

def retrieve_context(query, model_name="all-MiniLM-L6-v2", collection_name="articles"):
    model = SentenceTransformer(model_name)
    query_embedding = model.encode(query).tolist()

    # Qdrant and search
    client = QdrantClient(host="qdrant", port=6333)
    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=3
    )
    context = [result.payload.get("chunk", "") for result in results]
    return context

def query_ollama(prompt, model="llama3.1"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status() 
        return response.json()
    except Exception as e:
        return {"error": f"Error querying Ollama: {e}"}

if __name__ == "__main__":
    user_query = input("Enter your question: ")
    
    print("\nRetrieving relevant context from Qdrant...")
    retrieved_context = retrieve_context(user_query)
    
    if not retrieved_context:
        print("No relevant context found.")
    else:
        combined_context = " ".join(retrieved_context)
        prompt = (
            f"Question: \"{user_query}\"\n"
            f"Reference context: \"{combined_context}\"\n"
            "Can you answer the question using the reference context?"
        )
        
        print("\nQuerying Ollama with consolidated context...")
        result = query_ollama(prompt)
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print("\nFinal Response:")
            print(result['response'])
