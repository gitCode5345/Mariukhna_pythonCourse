import argparse
import csv
import logging
from consts import LOGGER_NAME
from time_utils import normalize_offset, offset_str_to_timezone
from datetime import datetime, timezone
from collections import defaultdict


def filter_data(csv_path: str, args: argparse):
    logger = logging.getLogger(LOGGER_NAME)
    filtered_data = []
    logger.info('Start filtering data')

    try:
        with open(csv_path, mode='r') as file:
            csv_reader = list(csv.DictReader(file))
            if args.gender:
                filtered_data = [data for data in csv_reader if data['gender'].lower() == args.gender.lower()]
            elif args.rows:
                filtered_data = [csv_reader[i] for i in range(args.rows)]

            logger.info('Data filtered successfully')
            return filtered_data
    except Exception as e:
        print(f'Exception {e}')
        logger.error(f'{e}')
        return None


def process_filtered_data(list_data: list[dict]):
    logger = logging.getLogger(LOGGER_NAME)
    name_rules = {'Mrs': 'missis', 'Ms': 'miss', 'Mr': 'mister', 'Madame': 'mademoiselle'}
    processed_data = []

    try:
        logger.info('Start processing filtered data')
        for index, element in enumerate(list_data, start=1):
            element['global_index'] = str(index)

            offset = element.get('location.timezone.offset', '+00:00')
            normalize_time = normalize_offset(offset)
            user_tz = offset_str_to_timezone(normalize_time)

            now_utc = datetime.now(timezone.utc)
            now_user_time = now_utc.astimezone(user_tz)
            element['current_time'] = now_user_time.strftime('%H:%M:%S')

            element['name.title'] = name_rules.get(element['name.title'], element['name.title'])

            if datetime.fromisoformat(element['dob.date']).year < 1960:
                continue
            element['dob.date'] = datetime.fromisoformat(element['dob.date']).strftime('%m-%d-%Y')
            element['registered.date'] = (datetime.fromisoformat(element['registered.date'])
                                          .strftime('%m-%d-%Y, %H:%M:%S'))

            processed_data.append(element)

        logger.info(f'{len(list_data)} data successfully processed')
        return processed_data
    except Exception as e:
        logger.error(e)


def group_data_by_year_country(data: list[dict]):
    logger = logging.getLogger(LOGGER_NAME)
    group_dict = defaultdict(lambda: defaultdict(list))

    logger.info('Start grouping data by years and countries')
    for item in data:
        country = item.get('location.country')
        year = datetime.strptime(item.get('dob.date'), '%m-%d-%Y').year
        decade = f'{year // 10 * 10}-th'
        group_dict[decade][country].append(item)

    logger.info('Data successfully grouped')
    return group_dict
