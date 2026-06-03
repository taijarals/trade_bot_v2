from foxbit_api import API_BASE # Importa a base da API
from settings import FOXBIT_KEY, FOXBIT_SECRET

API_BASE = "https://api.foxbit.com.br"


def gerar_assinatura(api_secret, method, path, params=None, body=""):
    """Gera a assinatura HMAC e cabeçalhos exigidos pela Foxbit."""

    timestamp = str(int(time.time() * 1000))

    queryString = urlencode(params) if params else ''

    rawBody = json.dumps(body) if body else ''

    preHash = f"{timestamp}{method.upper()}{path}{queryString}{rawBody}"

    assinatura = hmac.new(
        api_secret.encode(), preHash.encode(), hashlib.sha256
    ).hexdigest()

    headers = {
        "X-FB-ACCESS-KEY": FOXBIT_KEY,
        "X-FB-ACCESS-TIMESTAMP": timestamp,
        "X-FB-ACCESS-SIGNATURE": assinatura,
        "Content-Type": "application/json",
    }
    return headers


def chamada_api_privada(method, endpoint, payload=None, params=None):
    url = f"{API_BASE}{endpoint}"

    headers = gerar_assinatura(API_SECRET, method, endpoint, params, payload)

    try:
        response = requests.request(method, url, headers=headers, json=payload, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("📩 Resposta da API:", e.response.text)
        return None
