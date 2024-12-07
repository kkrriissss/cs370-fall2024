import json

def parse_nav2_docs(file_path):
    """Parse Nav2 data from JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cleaned_data = []
    for entry in data:
        cleaned_data.append({
            "title": entry.get("title", "No Title"),
            "content": entry.get("content", "").lower().strip(),
            "url": entry.get("url")
        })
    return cleaned_data
