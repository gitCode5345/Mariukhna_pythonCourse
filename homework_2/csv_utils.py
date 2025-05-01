import logging
import requests
import sys
import os


def download_csv(destination: str, filename: str):
    url = 'https://randomuser.me/api/?results=100&format=csv'
    logging.info(f'Downloading CSV data from {url}')
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(destination, filename + '.csv')
        with open(file_path, 'wb') as f:
            f.write(response.content)
        logging.info(f'Data saved to {file_path}')
        return file_path
    else:
        logging.error('Failed to download data')
        sys.exit(1)
