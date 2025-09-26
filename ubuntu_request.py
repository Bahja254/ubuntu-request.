import os
import requests
from urllib.parse import urlparse
import hashlib

def create_directory(directory="fetched-images"):
    """
    Create a directory if it does not exist.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def get_filename_from_url(url, directory="fetched-images"):
    """
    Extract filename from URL. 
    If not available, generate a unique filename using hash.
    Prevent duplicate downloads by checking existing files.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    if not filename:  
        # If URL doesn't end with a file name, generate one
        filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"

    filepath = os.path.join(directory, filename)
    
    # If file already exists, skip download
    if os.path.exists(filepath):
        print(f"⚠ Skipping: {filename} already exists.")
        return None
    
    return filepath

def download_image(url, directory="fetched-images"):
    """
    Download an image from the given URL and save it.
    Includes error handling and header checks.
    """
    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()  # Check HTTP errors

        # Check if the response is actually an image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"❌ Skipping {url} - not an image (Content-Type: {content_type})")
            return

        filepath = get_filename_from_url(url, directory)
        if filepath is None:
            return  # Duplicate image

        # Save image in binary mode
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"✅ Downloaded: {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")

def main():
    print("🌍 Ubuntu-Inspired Image Fetcher")
    print("I am because we are. Let's fetch images together.\n")

    urls = input("Enter one or more image URLs (comma-separated): ").split(",")

    directory = create_directory("fetched-images")

    for url in urls:
        url = url.strip()
        if url:
            download_image(url, directory)

if _name_ == "_main_":
    main()