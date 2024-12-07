import json
import os
import re

# Define paths
RAW_DATA_PATH = "../../data/raw/"
CLEANED_DATA_PATH = "../../data/cleaned/"

# Function to clean text
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

# Function to clean a JSON file
def clean_json_file(file_path, output_path):
    with open(file_path, 'r') as infile:
        data = json.load(infile)
    
    cleaned_data = []
    for entry in data:
        # Normalize fields
        cleaned_entry = {
            "title": clean_text(entry.get("title", "")),
            "url": entry.get("url", "").strip(),
            "content": clean_text(entry.get("content", ""))
        }
        # Skip empty entries
        if cleaned_entry["title"] and cleaned_entry["url"] and cleaned_entry["content"]:
            cleaned_data.append(cleaned_entry)
    
    # Remove duplicates
    cleaned_data = [dict(t) for t in {tuple(d.items()) for d in cleaned_data}]
    
    # Save cleaned data
    with open(output_path, 'w') as outfile:
        json.dump(cleaned_data, outfile, indent=4)
    print(f"Cleaned data saved to {output_path}")

# Main function to clean all data
def main():
    os.makedirs(CLEANED_DATA_PATH, exist_ok=True)

    # Define files to clean
    files_to_clean = {
        "ros2": "ros2_docs.json",
        "nav2": "nav2_tutorials.json",
        "moveit2": "moveit2_guides.json",
        "gazebo": "gazebo_resources.json"
    }
    
    for domain, filename in files_to_clean.items():
        raw_file = os.path.join(RAW_DATA_PATH, domain, filename)
        cleaned_file = os.path.join(CLEANED_DATA_PATH, f"{domain}_cleaned.json")
        print(f"Cleaning {raw_file}...")
        clean_json_file(raw_file, cleaned_file)

if __name__ == "__main__":
    main()
