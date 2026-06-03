def obter_ticker(symbol):
    """Obtém o preço atual de mercado (último preço) para o par informado."""
    endpoint = f"/rest/v3/markets/{symbol}/ticker/24hr"
    try:
        r = requests.get(API_BASE + endpoint)
        r.raise_for_status()
        data = r.json().get("data", {})

        df_ticker = pd.json_normalize(data)

        return df_ticker

    except Exception as e:
        print("❌ Erro ao consultar ticker:", e)
        return None

def resumir_ticker_df(df_ticker):
    last = df_ticker.iloc[-1]

    last_price = float(last["last_trade.price"])
    bid_price = float(last["best.bid.price"])
    ask_price = float(last["best.ask.price"])

    spread_pct = ((ask_price - bid_price) / last_price) * 100

    return {
        "preco_atual": last_price,
        "spread_pct": round(spread_pct, 4),
        "variacao_24h_pct": float(last["rolling_24h.price_change_percent"]),
        "volume_24h": float(last["rolling_24h.volume"]),
        "trades_24h": int(last["rolling_24h.trades_count"]),
        "max_24h": float(last["rolling_24h.high"]),
        "min_24h": float(last["rolling_24h.low"])
    }