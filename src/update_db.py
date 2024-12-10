import csv
import locale
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from models import Base, EmissionsData, EmissionsDataModel
from pydantic import ValidationError
from typing import List
import config
from helpers.data_cleaning import clean_row

# ----------------------
# Read and Validate Data
# ----------------------
def read_and_validate(file_path: str) -> List[EmissionsDataModel]:
    """
    Reads and validates data from the CSV file.

    Args:
        file_path (str): The path to the CSV file to read.

    Returns:
        List[EmissionsDataModel]: A list of validated EmissionsDataModel instances.
    """
    data_dict = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data_dict.append(dict(row))

    records = []
    for row in data_dict:
        try:
            cleaned_row = clean_row(row)
            record = EmissionsDataModel(**cleaned_row)
            records.append(record)
        except ValidationError as e:
            print(f"Validation error for row {row}: {e}")

    return records


# ----------------------
# Database Initialization
# ----------------------
def init_db() -> Engine:
    """
    Initializes the database by creating the tables and schema.

    Drops all existing tables and recreates the schema.

    Returns:
        Engine: The SQLAlchemy engine object used for database interaction.
    """
    engine = create_engine(config.DATABASE_URL)
    
    # Drop all tables and recreate schema
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    return engine


# ----------------------
# Insert Data into Database
# ----------------------
def insert_data(engine: Engine, records: List[EmissionsDataModel]) -> None:
    """
    Inserts a list of validated EmissionsDataModel records into the database.

    Args:
        engine (Engine): The SQLAlchemy engine object used to interact with the database.
        records (List[EmissionsDataModel]): A list of validated data records to insert into the database.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for record in records:
        db_record = EmissionsData(**record.model_dump())
        session.add(db_record)
    
    session.commit()
    session.close()


# ----------------------
# Main Script
# ----------------------
if __name__ == "__main__":
    # Set locale date as french for date parsing
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

    # Step 1: Validate data
    print("Reading, validating and cleaning data.")
    validated_records = read_and_validate(config.SOURCE_FILE_PATH)
    
    # Step 2: Initialize the database (drop and recreate the schema)
    print("Initializing db.")
    engine = init_db()

    # Step 3: Insert data into the database
    print("Inserting data into database.")
    insert_data(engine, validated_records)
    
    print("Done!")