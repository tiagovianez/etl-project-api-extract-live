import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base import and BitcoinPrice of database.py
from database import Base, BitcoinPrice

# Load environment variables from .env file
load_dotenv()

# Read separate variables from .env file (without SSL)
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Assemble the connection URL to the PostgreSQL database (without ?sslmode=...)
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Create the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_table():
    """Creates the table in the database if it does not exist."""
    Base.metadata.create_all(engine)
    print("Table created/verified successfully!")

def extract_bitcoin_data():
    """Extracts the full JSON from the Coinbase API."""
    url = 'https://api.coinbase.com/v2/prices/spot'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"API Error: {resposta.status_code}")
        return None

def process_bitcoin_data(json_data):
    """Transform API of raw data and adding timestamp"""
    value = float(json_data['data']['amount'])
    cryptocurrency = json_data['data']['base']
    currency = json_data['data']['currency']
    timestamp = datetime.now()
    
    transformed_data = {
        "value": value,
        "cryptocurrency": cryptocurrency,
        "currency": currency,
        "timestamp": timestamp
    }
    return transformed_data

def save_postgres_data(data):
    """Saves data in PostgreSQL database."""
    session = Session()
    new_register = BitcoinPrice(**data)
    session.add(new_register)
    session.commit()
    session.close()
    print(f"[{data['timestamp']}] saved data in the PostgreSQL!")

if __name__ == "__main__":
    create_table()
    print("Starting ETL with update for each 15 seconds... (press CTRL + C for interruption process)")
    while True:
        try:
            json_data = extract_bitcoin_data()
            if json_data:
                transformed_data = process_bitcoin_data(json_data)
                print("processed data:", transformed_data)
                save_postgres_data(transformed_data)
            time.sleep(15)
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Ending...")
            break
        except Exception as e:
            print(f"Error during execution: {e}")
            time.sleep(15)