import requests

def download_data(url, save_path):
    """Download data from the given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Data downloaded to {save_path}")
    else:
        print(f"Failed to download from {url}, Status Code: {response.status_code}")
