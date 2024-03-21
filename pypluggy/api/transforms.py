import datetime
import json
import re

ISO_DATE_REGEXP = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$')


def deserialize_json_with_dates(json_string: str) -> object:
    def custom_reviver(key, value):
        if isinstance(value, str) and ISO_DATE_REGEXP.match(value):
            return datetime.fromisoformat(value)
        return value

    return json.loads(json_string, object_hook=custom_reviver)
