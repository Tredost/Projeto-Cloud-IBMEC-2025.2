import base64
import requests
import time
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Configuração de autenticação
load_dotenv()
PRIVATE_KEY_PATH = 'test-prv-key.pem'
API_KEY = os.getenv("BINANCE_API_KEY")
if not API_KEY:
    raise ValueError("Erro: A chave da API não foi encontrada. Verifique o arquivo .env")

# Carregar a chave privada para assinatura
with open(PRIVATE_KEY_PATH, 'rb') as f:
    private_key = load_pem_private_key(data=f.read(), password=None)

# URL base da Binance Testnet
BASE_URL = "https://testnet.binance.vision"

def compra_venda(moeda: str, valor: float, operacao: bool):
    """
    Cria uma ordem de compra ou venda na Binance Testnet.

    Parâmetros:
        moeda (str): Nome da criptomoeda (ex: 'btc', 'eth').
        valor (float): Preço desejado para compra/venda.
        operacao (bool): True para compra, False para venda.

    Retorna:
        dict: Resposta da Binance sobre a ordem criada.
    """
    # Formatar o símbolo da moeda no padrão da Binance
    symbol = f"{moeda.upper()}USDT"

    # Determinar o tipo de operação
    side = "BUY" if operacao else "SELL"

    # Definir parâmetros da ordem
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': '1.0000000',  # Ajuste a quantidade conforme necessário
        'price': str(round(valor, 2)),
        'timestamp': int(time.time() * 1000),
    }

    # Assinar a requisição
    payload = '&'.join([f'{param}={value}' for param, value in params.items()])
    signature = base64.b64encode(private_key.sign(payload.encode('ASCII')))
    params['signature'] = signature

    # Enviar requisição para criar a ordem
    headers = {'X-MBX-APIKEY': API_KEY}
    response = requests.post(f'{BASE_URL}/api/v3/order', headers=headers, data=params)

    return response.json()

# Exemplo de uso
resultado = compra_venda("btc", 92000.00, True)  # Compra BTC a 92 mil dólares
print(resultado)

resultado = compra_venda("eth", 38000.00, False)  # Vende ETH a 38 mil dólares
print(resultado)

