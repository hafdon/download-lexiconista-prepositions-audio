import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# List of website URLs to process
urls = [
    "http://breistest.lexiconista.com/en/gram/faoi",
    # Add more URLs as needed
]

# Base URL for constructing MP3 links
BASE_MP3_URL = "http://breistest.lexiconista.com/"

# Dialects mapping (if needed for extensions)
DIALECTS = ['C', 'M', 'U']

def create_directories():
    """Create directories for each dialect if they don't exist."""
    for dialect in DIALECTS:
        os.makedirs(dialect, exist_ok=True)
        logging.debug(f"Directory '{dialect}' is ready.")

def extract_preposition(url):
    """Extract the preposition from the URL."""
    return url.rstrip('/').split('/')[-1]

def construct_mp3_url(preposition, dialect, word):
    """
    Construct the MP3 URL based on the dialect and word form.

    Example:
    For dialect 'C', word 'fúm', preposition 'faoi':
    http://breistest.lexiconista.com/CanC-preposition/f%C3%BAm.mp3
    """
    dialect_prefix = f"Can{dialect}-preposition"
    encoded_word = quote(word)
    mp3_url = urljoin(BASE_MP3_URL, f"{dialect_prefix}/{encoded_word}.mp3")
    return mp3_url

def download_mp3(mp3_url, dialect, preposition, word):
    """
    Download the MP3 file from mp3_url and save it to the appropriate directory.

    Filename format: "{Dialect}/{preposition}_{word}.mp3"
    """
    try:
        response = requests.get(mp3_url, stream=True)
        response.raise_for_status()
        filename = f"{preposition}_{word}.mp3"
        filepath = os.path.join(dialect, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Downloaded: {filepath}")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred while downloading {mp3_url}: {http_err}")
    except Exception as err:
        logging.error(f"Error occurred while downloading {mp3_url}: {err}")

def parse_and_download(url):
    """Parse the webpage and download all associated MP3s."""
    logging.info(f"Processing URL: {url}")
    preposition = extract_preposition(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred while fetching {url}: {http_err}")
        return
    except Exception as err:
        logging.error(f"Error occurred while fetching {url}: {err}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all divs with class 'line' containing the word forms and buttons
    lines = soup.find_all('div', class_='line')

    for line in lines:
        # Extract the word form
        word_span = line.find('span', class_='value primary')
        if not word_span:
            continue
        word = word_span.text.strip()
        if not word:
            continue

        # Find all dialect buttons within the line
        buttons = line.find_all('button', class_='sound')
        for button in buttons:
            # Extract dialect from the button text or attributes
            dialect = button.text.strip()
            if dialect not in DIALECTS:
                logging.warning(f"Unknown dialect '{dialect}' for word '{word}'. Skipping.")
                continue

            # Construct the MP3 URL
            mp3_url = construct_mp3_url(preposition, dialect, word)

            # Download the MP3
            download_mp3(mp3_url, dialect, preposition, word)

def main():
    create_directories()
    for url in urls:
        parse_and_download(url)
    logging.info("All downloads completed.")

if __name__ == "__main__":
    main()
