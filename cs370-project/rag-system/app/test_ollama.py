import requests


OLLAMA_API_URL = "http://172.17.0.1:54321/api/generate"

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
    user_query = "Hello, how are you?"

    print("Querying Ollama...")
    result = query_ollama(user_query)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Response: {result['response']}")
        print(f"Metadata: {result}")
