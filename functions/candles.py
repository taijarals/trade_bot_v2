def pegar_candlesticks(symbol, interval, limit):
    endpoint = f"/rest/v3/markets/{symbol}/candlesticks"
    params = {"interval": interval, "limit": limit}

    response = requests.get(API_BASE + endpoint, params=params)
    if response.status_code != 200:
        print(f"❌ Erro ao obter candlesticks. Status code: {response.status_code}")
        print("Resposta bruta:", response.text)
        raise Exception("Erro na API ao obter candlesticks.")

    candles = response.json() # lista de listas

    df = pd.DataFrame(candles, columns=[
        "timestamp_open", "open", "high", "low", "close",
        "timestamp_close", "volume", "quoteVolume", "count",
        "takerBuyVolume", "takerBuyQuoteVolume"
    ])

    # Converter timestamps para datetime legível
    df["timestamp_open"] = pd.to_datetime(df["timestamp_open"], unit='ms')
    df["timestamp_close"] = pd.to_datetime(df["timestamp_close"], unit='ms')

    return df

def resumir_candles(df, n=20):
    import pandas as pd
    import numpy as np

    df = df.tail(n).copy()

    # garante tipo numérico
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    # remove possíveis NaNs
    df = df.dropna(subset=["close"])

    # validação mínima
    if len(df) < 2:
        return {
            "preco_atual": None,
            "retorno_curto_pct": None,
            "volatilidade_pct": None,
            "tendencia_curta": None,
            "rsi_14": None,
            "distancia_sma_20_pct": None
        }

    # =========================
    # PREÇOS
    # =========================
    preco_atual = df.iloc[-1]["close"]
    preco_inicial = df.iloc[0]["close"]

    retorno_pct = ((preco_atual - preco_inicial) / preco_inicial) * 100

    volatilidade_pct = df["close"].pct_change().std() * 100

    # =========================
    # RSI 14
    # =========================
    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    # evita divisão por zero sem perder pandas.Series
    rs = avg_gain / avg_loss.replace(0, np.nan)

    rsi = 100 - (100 / (1 + rs))

    # quando não houver perdas, RSI tende a 100
    rsi = rsi.fillna(100)

    rsi_atual = rsi.iloc[-1]

    # =========================
    # SMA 20
    # =========================
    sma_20 = (
        df["close"].rolling(window=20).mean().iloc[-1]
        if len(df) >= 20
        else np.nan
    )

    distancia_sma_pct = None

    if not pd.isna(sma_20):
        distancia_sma_pct = (
            ((preco_atual - sma_20) / sma_20) * 100
        )

    # =========================
    # TENDÊNCIA
    # =========================
    if retorno_pct > 0.2:
        tendencia = "alta"

    elif retorno_pct < -0.2:
        tendencia = "baixa"

    else:
        tendencia = "lateral"

    # =========================
    # RETORNO
    # =========================
    return {
        "preco_atual": round(float(preco_atual), 4),

        "retorno_curto_pct": round(float(retorno_pct), 3),

        "volatilidade_pct": (
            None
            if pd.isna(volatilidade_pct)
            else round(float(volatilidade_pct), 3)
        ),

        "tendencia_curta": tendencia,

        "rsi_14": (
            None
            if pd.isna(rsi_atual)
            else round(float(rsi_atual), 2)
        ),

        "distancia_sma_20_pct": (
            None
            if distancia_sma_pct is None or pd.isna(distancia_sma_pct)
            else round(float(distancia_sma_pct), 3)
        )
    }