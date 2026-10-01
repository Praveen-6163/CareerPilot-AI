import json
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
RESOURCE_PATH = os.path.join(ROOT, 'data', 'resources.json')


def load_resource_catalog():
    try:
        with open(RESOURCE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def get_resources_for_topic(topic):
    items = []
    for category in load_resource_catalog():
        if isinstance(category, dict):
            category_name = str(category.get('category', '')).lower()
            if topic.lower() in category_name or category_name in topic.lower():
                items.extend(category.get('items', []))
    return items[:5]


def get_resources_by_category(category):
    for category_group in load_resource_catalog():
        if str(category_group.get('category', '')).lower() == str(category).lower():
            return category_group.get('items', [])
    return []
