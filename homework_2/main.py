import argparse
from csv_utils import fetch_data_and_save_to_csv, save_processed_data_to_csv, save_grouped_data_by_year_country_to_csv
from consts import LOGGER_NAME
from data_processing import filter_data, process_filtered_data, group_data_by_year_country
from logging_operations import log_folder_structure
from pathlib import Path
from logging_operations import setup_logger
from zip_utils import archive_folder


def setup_arg_parse():
    arguments = argparse.ArgumentParser()

    arguments.add_argument('--destination', type=str,
                           help='Path to a folder where output file is going to be placed', required=True)
    arguments.add_argument('--filename', type=str, default='lab_3_file.csv', help='File name\
                           (default \'lab_3_file.csv\')')

    group_arguments = arguments.add_mutually_exclusive_group(required=True)
    group_arguments.add_argument('--gender', type=str, help='Gender to filter the data by')
    group_arguments.add_argument('--rows', type=int, help='Number of rows to filter by')

    arguments.add_argument('--log_level', type=str, default='DEBUG', help="Set the level of debug output")

    return arguments.parse_args()


def main():
    args = setup_arg_parse()
    setup_logger(LOGGER_NAME, args.log_level)

    full_csv_path = f'{args.destination}/{args.filename}'
    fetch_data_and_save_to_csv(full_csv_path)
    filtered_data = filter_data(full_csv_path, args)
    processed_data = process_filtered_data(filtered_data)
    save_processed_data_to_csv(args.destination, 'filtered.csv', processed_data)
    grouped_data = group_data_by_year_country(processed_data)
    save_grouped_data_by_year_country_to_csv(args.destination, grouped_data)

    log_folder_structure(Path(args.destination))
    archive_folder(args.destination, 'people_data')


if __name__ == '__main__':
    main()
