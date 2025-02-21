import base64
import requests
import time
from dotenv import load_dotenv
import os
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Set up authentication
load_dotenv()
PRIVATE_KEY_PATH='test-prv-key.pem'
API_KEY = os.getenv("BINANCE_API_KEY")
if not API_KEY:
    raise ValueError("Erro: A chave da API não foi encontrada. Verifique o arquivo .env")

# Load the private key.
with open(PRIVATE_KEY_PATH, 'rb') as f:
    private_key = load_pem_private_key(data=f.read(),
                                       password=None)

# URL base da API Binance
BASE_URL = "https://api.binance.com"

# Obter o preço atual do BTC
ticker_url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
response = requests.get(ticker_url)
btc_price = float(response.json()['price'])

# Definir um preço válido (por exemplo, 1% abaixo do mercado)
valid_price = round(btc_price * 0.99, 2)  # 1% abaixo e arredondado para 2 casas decimais
print(f"Preço válido: {valid_price}")
print(f"Preço atual: {btc_price}")
'''
# Set up the request parameters
params = {
    'symbol': 'BTCUSDT',
    'side': 'SELL',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': '1.0000000',
    'price': str(valid_price),  # ✅ Preço ajustado
}

# Timestamp the request
timestamp = int(time.time() * 1000) # UNIX timestamp in milliseconds
params['timestamp'] = timestamp

# Sign the request
payload = '&'.join([f'{param}={value}' for param, value in params.items()])
signature = base64.b64encode(private_key.sign(payload.encode('ASCII')))
params['signature'] = signature

# Send the request
headers = {
    'X-MBX-APIKEY': API_KEY,
}
response = requests.post(
    'https://testnet.binance.vision/api/v3/order',
    headers=headers,
    data=params,
)
print(response.json())'''