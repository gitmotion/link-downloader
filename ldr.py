import os
import sys
import requests
from urllib.parse import urlparse

def download_file(url, directory):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Parse the URL to get the file name
        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path)

        # Create the full file path
        file_path = os.path.join(directory, file_name)

        # Write the file to the specified directory
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded: {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def main(urls_file, download_directory):
    # Ensure the download directory exists
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Read URLs from the file
    with open(urls_file, 'r') as file:
        urls = file.readlines()

    # Download each file
    for url in urls:
        url = url.strip()  # Remove any surrounding whitespace
        if url:
            download_file(url, download_directory)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_files.py <urls_file.txt> <download_directory>")
        sys.exit(1)

    urls_file = sys.argv[1]
    download_directory = sys.argv[2]

    main(urls_file, download_directory)

