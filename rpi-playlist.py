import requests
import os
import csv
import json

# Constants for file paths
CONFIG_FILE = 'config.json'
MEDIA_FOLDER = './media'
PLAYLIST_FILE = 'playlist.csv'

#Load RPI_ID and database configuration from an external JSON file
def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

# Load configuration
config = load_config()

# Download a file from a URL and save it locally
def download_file(url, local_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        exit(1)

# Fetch media items from the URL API based on RPI_ID
def fetch_media_from_api():
    try:
        response = requests.get(config['api_url'], params={
            'token': config['token'],
            'rpitv_id': config['rpi_id']
        })
        response.raise_for_status()
        media_items = response.json()
        return media_items
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        exit(1)

# Clean up old files in the media directory
def clean_up_old_files(current_files):
    for filename in os.listdir(MEDIA_FOLDER):
        file_path = os.path.join(MEDIA_FOLDER, filename)
        if file_path not in current_files:
            print(f"Removing old file: {file_path}")
            os.remove(file_path)

# Update the playlist by fetching media items from the database and downloading files locally
def update_playlist():
    print("Updating playlist...")
    media_items = fetch_media_from_api()

    # Ensure the media folder exists
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)

    # Track current files
    current_files = set()

    # Open the playlist file for writing
    with open(PLAYLIST_FILE, 'w', newline='') as csvfile:
        fieldnames = ['media_type', 'file_path', 'display_time', 'display_order']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each media item
        for item in media_items:
            file_url = item['file_path']
            local_path = os.path.join(MEDIA_FOLDER, os.path.basename(file_url))
            current_files.add(local_path)

            # Download the file if it doesn't already exist
            if not os.path.exists(local_path):
                print(f"Downloading {file_url} to {local_path}")
                download_file(file_url, local_path)

            # Write the media item to the playlist file
            writer.writerow({
                'media_type': item['media_type'],
                'file_path': local_path,
                'display_time': item['display_time'],
                'display_order': item['display_order']
            })

    # Clean up old files in the media directory
    clean_up_old_files(current_files)

    print("Playlist updated!")

if __name__ == '__main__':
    update_playlist()
