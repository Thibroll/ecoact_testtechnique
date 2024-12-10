from datetime import datetime
from typing import List, Dict, Optional
from helpers.mapping import column_name_mapping


def convert_to_datetime(value: Optional[str], date_format: str = '%B %Y') -> Optional[datetime]:
    """Convert a string to a datetime object if valid."""
    if isinstance(value, str):
        try:
            # Handle specific case for 'Decembre' replacement
            if 'Decembre' in value:
                value = value.replace('Decembre', 'Décembre')
            return datetime.strptime(value, date_format)
        except ValueError as e:
            print(f"Error converting date string '{value}': {e}")
            return None
    return None

def clean_categorie(categories: Optional[str]) -> List[str]:
    if categories is None:
        return []
    return categories.split(" > ")

def clean_tags(tags: Optional[str]) -> List[str]:
    """Clean the 'Tags français' column by splitting and stripping tags."""
    if isinstance(tags, str):
        try:
            return [tag.strip() for tag in tags.split(',')]
        except ValueError as e:
            print(f"Error cleaning tags: {tags} ; Error: {e}")
    return []

def clean_row(row: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """Clean the row dictionary by converting columns and cleaning data"""

    #process empty strings to force none values
    row = {key: (value if value != "" else None) for key, value in row.items()}

    #map the row key values
    row = {column_name_mapping.get(k, k): v for k, v in row.items()}

    row['date_creation'] = convert_to_datetime(row.get('date_creation'))
    row['date_modification'] = convert_to_datetime(row.get('date_modification'))
    row['code_categorie'] = clean_categorie(row.get('code_categorie'))

        # Décomposition du code catégorie pour les stocker dans des colonnes
    for i in range(5):
        row[f'code{i+1}'] = row['code_categorie'][i] if len(row['code_categorie']) > i else None

    row['tags_francais'] = clean_tags(row.get('tags_francais'))

    return row