import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:dbpassword123@localhost:5432/ecoact_db")
SOURCE_FILE_PATH = os.getenv("SOURCE_FILE_PATH", "data/donnees_candidats_dev_python.xlsx")