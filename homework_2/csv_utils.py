import csv
import logging
import requests
import os
from consts import DATA_URL, LOGGER_NAME
from collections import Counter


def fetch_data_and_save_to_csv(full_save_path: str):
    logger = logging.getLogger(LOGGER_NAME)
    response = requests.get(DATA_URL)
    logger.info(f'Start collecting data from: {DATA_URL}')

    if response.status_code == 200:
        with open(full_save_path, mode='wb') as file:
            file.write(response.content)
        logger.info(f'Data successfully saved to: {full_save_path}')
    else:
        logger.error('Failed to load data.')
        return


def save_processed_data_to_csv(path: str, filename: str, list_data: list[dict]):
    logger = logging.getLogger(LOGGER_NAME)
    full_save_path = f'{path}/{filename}'

    try:
        headers = list_data[0].keys()
        with open(full_save_path, mode='w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(list_data)
    except Exception as e:
        print(e)
        logger.error(e)


def save_grouped_data_by_year_country_to_csv(path: str, data):
    logger = logging.getLogger(LOGGER_NAME)
    logger.info('Start saving grouped data to file')
    for decade, countries in data.items():
        os.makedirs(f'{path}/{decade}', exist_ok=True)
        for country, users in countries.items():
            os.makedirs(f'{path}/{decade}/{country}', exist_ok=True)

            try:
                max_age = max(int(user['dob.age']) for user in users)
                avg_years = sum(int(user['registered.age']) for user in users) // len(users)
                common_id = Counter(user['id.name'] for user in users).most_common(1)[0][0]
            except Exception as e:
                logging.warning(f'Skipping group {decade}/{country} due to error: {e}')
                continue

            filename = f'max_age_{max_age}_avg_registered_{avg_years}_popular_id_{common_id}.csv'
            file_path = f'{path}/{decade}/{country}/{filename}'

            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                csv_writer = csv.DictWriter(file, fieldnames=users[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(users)

            logger.info(f'Data saved until: {file_path}')
