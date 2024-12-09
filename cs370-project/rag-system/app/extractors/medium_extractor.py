import requests
from bs4 import BeautifulSoup
import json

def crawl_medium_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title and content
        title = soup.find('h1').get_text() if soup.find('h1') else "No Title Found"
        content = ' '.join([p.get_text() for p in soup.find_all('p')])

        return {
            "title": title,
            "content": content,
            "source": "Medium",
            "metadata": {"url": url}
        }
    except Exception as e:
        print(f"Error crawling Medium article at {url}: {e}")
        return None


def read_links(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_to_json(data, file_path):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved successfully to {file_path}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

if __name__ == "__main__":
    links_file = "extractors/links_to_crawl.txt"
    output_file = "extractors/extracted_articles.json"
    links = read_links(links_file)

    extracted_data = []
    for url in links:
        if "medium.com" in url:
            article_data = crawl_medium_article(url)
            if article_data:
                extracted_data.append(article_data)

    save_to_json(extracted_data, output_file)