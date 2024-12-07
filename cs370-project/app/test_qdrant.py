import requests

try:
    response = requests.get("http://qdrant:6333/health")
    print("Raw Response:")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except requests.exceptions.JSONDecodeError:
    print("Request failed: Unable to parse JSON response")
