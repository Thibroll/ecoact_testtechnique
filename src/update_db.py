import pandas as pd
import locale
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from models import Base, CandidateData, CandidateDataModel
from pydantic import ValidationError
import config
import mapping
from helpers.data_cleaning import clean_row

# ----------------------
# Read and Validate Data
# ----------------------
def read_and_validate(file_path):
    df = pd.read_excel(file_path)
    df = df.rename(columns=mapping.column_name_mapping)
    records = []
    
    for _, row in df.sample().iterrows():
        try:
            row = clean_row(row)
            record = CandidateDataModel(**row.to_dict())
            records.append(record)
        except ValidationError as e:
            print(f"Validation error: {e}")

    return records


# ----------------------
# Database Initialization
# ----------------------
def init_db():
    engine = create_engine(config.DATABASE_URL)
    
    # Drop all tables and recreate schema (if you prefer this approach)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    return engine


# ----------------------
# Empty the Table Before Inserting Data
# ----------------------
def empty_table(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    inspector = inspect(engine)
    if 'candidate_data' in inspector.get_table_names():
        print("Table 'candidate_data' found, removing it to insert again the data.")
        try:
            # Execute TRUNCATE only if the table exists
            session.execute(text("TRUNCATE TABLE candidate_data RESTART IDENTITY CASCADE;"))
            session.commit()
            print("Table 'candidate_data' successfully truncated.")
        except Exception as e:
            print(f"Error emptying the table: {e}")
        finally:
            session.close()


# ----------------------
# Insert Data into Database
# ----------------------
def insert_data(engine, records):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for record in records:
        db_record = CandidateData(**record.dict())
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
    print("Reading and validating data.")
    validated_records = read_and_validate(config.SOURCE_FILE_PATH)
    
    # Step 2: Initialize the database (drop and recreate the schema)
    print("Initializing db.")
    engine = init_db()

    # Step 3: Empty the existing table (before inserting new data)
    print("Emptying existing table (if exists)")
    empty_table(engine)
    
    # Step 4: Insert data into the database
    print("Inserting data into database.")
    insert_data(engine, validated_records)
    
    print("Done!")