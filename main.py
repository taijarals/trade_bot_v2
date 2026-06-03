import os
import pandas as pd
import json
import requests
import pandas as pd
import time
import hmac
import hashlib
import json
import requests
from urllib.parse import urlencode
import numpy as np
from functions.analises import montar_contexto_mercado
from functions.candles import pegar_candlesticks
from functions.ia import analisar_mercado
from functions.ticker import obter_ticker
from functions.orderbook import obter_orderbook


df_candles = pegar_candlesticks("btcbrl", "1m", "10")
df_ticker = obter_ticker("btcbrl")
df_orderbook = obter_orderbook("btcbrl")

contexto_mercado = montar_contexto_mercado(df_candles, df_ticker, df_orderbook )

#contexto_mercado

def analisar_mercado_wrapper(contexto_mercado):
    resposta_texto = analisar_mercado(contexto_mercado, client)
    return resposta_texto

decisao = analisar_mercado_wrapper(contexto_mercado)
print(decisao)