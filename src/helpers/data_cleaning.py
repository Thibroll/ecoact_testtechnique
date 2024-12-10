from datetime import datetime
from typing import List, Dict, Optional
from helpers.mapping import column_name_mapping


def convert_to_datetime(value: Optional[str], date_format: str = '%B %Y') -> Optional[datetime]:
    """
    Converts a string to a datetime object if the string matches the specified format.
    
    This function handles the conversion of string values like "December 2021" into 
    a `datetime` object. It also includes a specific fix for the French spelling of 
    December ("Decembre" to "Décembre").

    Args:
        value (Optional[str]): The string value to be converted.
        date_format (str): The format used to parse the string into a `datetime` object. Defaults to '%B %Y'.
    
    Returns:
        Optional[datetime]: The converted `datetime` object if the string was valid; otherwise, `None`.
    """
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
    """
    Splits a category string into a list of categories.
    
    Args:
        categories (Optional[str]): The category string to be split (e.g., "A > B > C").
    
    Returns:
        List[str]: A list of category strings (e.g., ["A", "B", "C"]).
    """
    if categories is None:
        return []
    return categories.split(" > ")

def clean_tags(tags: Optional[str]) -> List[str]:
    """
    Cleans the 'Tags français' column by splitting and stripping tags.
    
    Args:
        tags (Optional[str]): A string of tags separated by commas (e.g., "tag1, tag2, tag3").
    
    Returns:
        List[str]: A list of cleaned tags (e.g., ["tag1", "tag2", "tag3"]).
    
    Raises:
        ValueError: If the tags string is malformed, an error will be logged.
    """
    if isinstance(tags, str):
        try:
            return [tag.strip() for tag in tags.split(',')]
        except ValueError as e:
            print(f"Error cleaning tags: {tags} ; Error: {e}")
    return []

def clean_row(row: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """
    Cleans a data row by processing and mapping the fields to their correct format.
    
    This function processes each column in the row, applying various cleaning and
    conversion methods, such as converting dates to `datetime` objects and cleaning
    categories and tags. It also handles empty strings and applies a column name mapping.

    Args:
        row (Dict[str, Optional[str]]): The row data as a dictionary where keys are column names
                                         and values are corresponding data values (strings or None).
    
    Returns:
        Dict[str, Optional[str]]: The cleaned row with the necessary conversions and mappings.
    """

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