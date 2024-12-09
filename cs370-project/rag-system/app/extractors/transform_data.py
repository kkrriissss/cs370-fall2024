import json
import re


def clean_content(content):
    content = re.sub(r"(Sign up Sign in\s)+", "", content)
    content = content.replace("\u2014", "-")
    
    # Remove extra whitespace
    content = content.strip()
    return content


def clean_data(data):
    cleaned_data = []
    for item in data:
        # Clean title and content
        item["title"] = item["title"].strip() if item.get("title") else "No Title"
        item["content"] = clean_content(item["content"]) if item.get("content") else "No Content"
        
        # Add cleaned item to list
        cleaned_data.append(item)
    return cleaned_data


def save_to_json(data, file_path):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Cleaned data saved successfully to {file_path}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")


if __name__ == "__main__":
    extracted_file = "extractors/extracted_articles.json"
    transformed_file = "extractors/transformed_articles.json"
    
    try:
        with open(extracted_file, "r") as f:
            extracted_data = json.load(f)
    except Exception as e:
        print(f"Error loading extracted data: {e}")
        extracted_data = []

    # Clean and normalize data
    cleaned_data = clean_data(extracted_data)
    save_to_json(cleaned_data, transformed_file)
