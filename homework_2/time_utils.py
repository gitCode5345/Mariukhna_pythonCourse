from datetime import timezone, timedelta
import re


def normalize_offset(offset_str):
    if offset_str.upper() == 'Z':
        return '+00:00'
    if not offset_str.startswith(('+', '-')):
        offset_str = f'+{offset_str}'
    parts = offset_str[1:].split(':')
    if len(parts) == 2:
        hours = parts[0].zfill(2)
        minutes = parts[1].zfill(2)
        return offset_str[0] + hours + ':' + minutes
    raise ValueError(f'Invalid offset string: {offset_str}')


def offset_str_to_timezone(offset_str):
    if offset_str.upper() == 'Z':
        return timezone.utc

    match = re.match(r'([+-])(\d{2}):(\d{2})', offset_str)
    if not match:
        raise ValueError(f'Invalid offset format: {offset_str}')

    sign, hours, minutes = match.groups()
    delta = timedelta(hours=int(hours), minutes=int(minutes))
    if sign == '-':
        delta = -delta

    return timezone(delta)
