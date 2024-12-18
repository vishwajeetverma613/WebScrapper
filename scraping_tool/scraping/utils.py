import os
import requests

def save_image(url, path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(f"Error saving image {url}: {e}")
