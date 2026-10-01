import json
import os
from typing import Any, Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def read_json(file_name: str, default=None):
    ensure_data_dir()
    path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path):
        if default is not None:
            write_json(file_name, default)
            return default
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default if default is not None else []


def write_json(file_name: str, payload: Any):
    ensure_data_dir()
    path = os.path.join(DATA_DIR, file_name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
        f.write('\n')
    return True


def update_json(file_name: str, payload: Any):
    return write_json(file_name, payload)


def append_record(file_name: str, record: Dict[str, Any]):
    items = read_json(file_name, [])
    if not isinstance(items, list):
        items = []
    items.append(record)
    write_json(file_name, items)
    return record


def delete_record(file_name: str, record_id: str):
    items = read_json(file_name, [])
    if not isinstance(items, list):
        return False
    filtered = [item for item in items if str(item.get('id')) != str(record_id)]
    write_json(file_name, filtered)
    return True


def find_records(file_name: str, key: str, value: Any):
    items = read_json(file_name, [])
    if not isinstance(items, list):
        return []
    return [item for item in items if item.get(key) == value]
