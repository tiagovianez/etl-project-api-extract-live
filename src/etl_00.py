import requests
from tinydb import TinyDB
from datetime import datetime



def data_extract_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    data = response.json()
    return data

def data_transform_bitcoin(data):
    value = data["data"]["amount"]
    cryptocurrency = data["data"]["base"]
    currency = data["data"]["currency"]
    timestamp = datetime.now().timestamp()

    transformed_data = {
        "value": value,
        "cryptocurrency": cryptocurrency,
        "currency": currency,
        "timestamp": timestamp
    }

    return transformed_data

def data_save_tinydb(data, db_name="bitcoin.json"):
    db = TinyDB(db_name)
    db.insert(data)
    print("data saved successfully!")


if __name__ == "__main__":
    # Data extraction
    data_json = data_extract_bitcoin()
    treatment_data = data_transform_bitcoin(data_json)
    data_save_tinydb(treatment_data)