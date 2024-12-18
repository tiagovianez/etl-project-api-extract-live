import requests

url = "https://api.coinbase.com/v2/prices/spot"
headers = {
    "Accept": "application/json",
    "User-Agent": "myApplication/1.0"
}
params = {"currency": "USD"}  # query currency

response = requests.get(url, headers=headers, params=params)
data = response.json()
print("Bitcoin price(USD):", data["data"]["amount"])