import argparse
import logging
import os
import sys
from pathlib import Path
from csv_utils import download_csv
from prepare_user_data import preprocess_data, group_users, save_grouped_data, log_folder_structure, archive_folder


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', help='Destination folder')
    parser.add_argument('--filename', default='output', help='Output filename (default: output)')
    parser.add_argument('--gender', help='Filter by gender')
    parser.add_argument('--rows', type=int, help='Limit number of rows')
    parser.add_argument('log_level', nargs='?', default='INFO', help='Logging level')
    return parser.parse_args()


def setup_logger(setup_args, log_level='INFO'):
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(setup_args.destination, 'script.log')),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    args = parse_args()
    setup_logger(args, args.log_level)

    os.makedirs(args.destination, exist_ok=True)
    os.chdir(args.destination)

    csv_path = download_csv('.', args.filename)
    data = preprocess_data(csv_path, gender=args.gender, rows=args.rows)
    grouped = group_users(data)
    save_grouped_data(grouped, '.')

    log_folder_structure(Path('.'))
    archive_folder(os.path.abspath('.'), 'user_data')


if __name__ == '__main__':
    main()
