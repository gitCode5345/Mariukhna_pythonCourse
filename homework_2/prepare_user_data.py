import logging
import shutil
import csv
from datetime import datetime, timedelta, timezone
from collections import defaultdict, Counter
from pathlib import Path


def preprocess_data(file_path, gender=None, rows=None):
    processed_data = []
    title_map = {'Mrs': 'missis', 'Ms': 'miss', 'Mr': 'mister', 'Madame': 'mademoiselle'}

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            if gender and row['gender'] != gender:
                continue

            row['global_index'] = str(i)
            offset_str = row.get('location.timezone.offset', '+00:00')

            try:
                sign = 1 if offset_str.startswith('+') else -1
                offset_parts = offset_str[1:].split(':')
                hours_offset = int(offset_parts[0])
                minutes_offset = int(offset_parts[1]) if len(offset_parts) > 1 else 0
                tz = timezone(sign * timedelta(hours=hours_offset, minutes=minutes_offset))
                user_time = datetime.now(tz).isoformat()
            except Exception as e:
                logging.warning(f'Failed to parse timezone {offset_str}, defaulting to UTC: {e}')
                user_time = datetime.now(timezone.utc).isoformat()

            row['current_time'] = user_time

            title = row['name.title']
            row['name.title'] = title_map.get(title, title)

            # Parse and reformat dates
            try:
                dob_date = datetime.fromisoformat(row['dob.date'].replace('Z', '+00:00'))
                reg_date = datetime.fromisoformat(row['registered.date'].replace('Z', '+00:00'))
            except Exception:
                continue

            if dob_date.year < 1960:
                continue

            row['dob.date'] = dob_date.strftime('%m/%d/%Y')
            row['registered.date'] = reg_date.strftime('%m-%d-%Y, %H:%M:%S')

            processed_data.append(row)

            if rows and len(processed_data) >= rows:
                break

    fieldnames = list(processed_data[0].keys()) if processed_data else []
    with open(file_path, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)

    logging.info(f'Preprocessed {len(processed_data)} rows')
    return processed_data


def group_users(data):
    grouped = defaultdict(lambda: defaultdict(list))
    for row in data:
        dob = datetime.strptime(row['dob.date'], '%m/%d/%Y')
        decade = f'{dob.year // 10 * 10}-th'
        country = row['location.country']
        grouped[decade][country].append(row)
    return grouped


def save_grouped_data(grouped, base_path):
    for decade, countries in grouped.items():
        decade_path = Path(base_path) / decade
        decade_path.mkdir(parents=True, exist_ok=True)

        for country, users in countries.items():
            country_path = decade_path / country
            country_path.mkdir(parents=True, exist_ok=True)

            # Calculate required values
            try:
                max_age = max(int(user['dob.age']) for user in users)
                avg_years = sum(int(user['registered.age']) for user in users) // len(users)
                common_id = Counter(user['id.name'] for user in users).most_common(1)[0][0]
            except Exception as e:
                logging.warning(f'Skipping group {decade}/{country} due to error: {e}')
                continue

            filename = f'max_age_{max_age}_avg_registered_{avg_years}_popular_id_{common_id}.csv'
            file_path = country_path / filename

            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=users[0].keys())
                writer.writeheader()
                writer.writerows(users)

            logging.info(f'Saved file: {file_path}')


def log_folder_structure(path: Path, level=0):
    for item in sorted(path.iterdir()):
        prefix = '    ' * level + ('[FOLDER] ' if item.is_dir() else '[FILE] ')
        logging.info(f'{prefix}{item.name}')
        if item.is_dir():
            log_folder_structure(item, level + 1)


def archive_folder(folder_path, name_zip):
    archive_name = shutil.make_archive(name_zip, 'zip', folder_path)
    logging.info(f'Folder archived: {archive_name}')
