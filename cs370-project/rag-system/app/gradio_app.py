import gradio as gr
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import requests

OLLAMA_API_URL = "http://172.17.0.1:54321/api/generate"

def retrieve_context(query, model_name="all-MiniLM-L6-v2", collection_name="articles"):
    """
    Retrieve relevant context chunks from Qdrant for the given query.
    """
    model = SentenceTransformer(model_name)
    query_embedding = model.encode(query).tolist()
    client = QdrantClient(host="qdrant", port=6333)
    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=3
    )
    return [result.payload.get("chunk", "") for result in results]

def query_ollama(prompt, model="llama3.1"):
    payload = {"model": model, "prompt": prompt, "stream": False}
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json().get("response", "No response from the model")
    except Exception as e:
        return f"Error querying Ollama: {e}"

def process_query(user_query):
    context_chunks = retrieve_context(user_query)
    if not context_chunks:
        return "No relevant context found."
    combined_context = " ".join(context_chunks)
    prompt = (
        f"Question: \"{user_query}\"\n"
        f"Reference context: \"{combined_context}\"\n"
        "Can you answer the question using the reference context?"
    )
    response = query_ollama(prompt)
    return response

def gradio_interface(question):
    response = process_query(question)
    return response

#app layout
with gr.Blocks() as app:
    gr.Markdown("# CS-370 Project: Kriss Sitapara & Paridhi Bhardwaj")
    gr.Markdown("Ask a question about your dataset and get an answer based on the retrieved context.")
    
    # Input and output
    question = gr.Textbox(label="Enter your question", placeholder="How do I start using ROS2?")
    response = gr.Textbox(label="Model Response", placeholder="The model's response will appear here.", lines=6)
    submit_btn = gr.Button("Submit")
    submit_btn.click(gradio_interface, inputs=[question], outputs=[response])

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=True)
