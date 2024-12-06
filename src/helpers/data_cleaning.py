from datetime import datetime
import pandas as pd

def convert_to_datetime(value, date_format='%B %Y'):
    """Convert a string to a datetime object if valid."""
    try:
        if 'Decembre' in value:
            value.replace('Decembre', 'Décembre')
        return datetime.strptime(value, date_format) if isinstance(value, str) else None
    except ValueError as e:
        print(f"Error converting date string '{value}': {e}")
        return None

def clean_tags(tags):
    """Clean the 'Tags français' column by splitting and stripping tags."""
    try:
        if isinstance(tags, str):
            return [tag.strip() for tag in tags.split(',')]
    except ValueError as e:
        print(f"Error cleaning tags : {tags} ; Error : {e}")
    return []

def clean_row(row: pd.Series):
    """Clean the row by converting date columns and cleaning 'Tags français'."""
    row['date_creation'] = convert_to_datetime(row.get('date_creation'))
    row['date_modification'] = convert_to_datetime(row.get('date_modification'))
    row['Tags français'] = clean_tags(row.get('Tags français'))
    return row