def obter_orderbook(symbol):
    """Obtém o livro de ordens (orderbook) para o par informado."""
    endpoint = f"/rest/v3/markets/{symbol}/orderbook"

    params = {"level": 5}

    try:
        r = requests.get(API_BASE + endpoint)
        r.raise_for_status()
        data = r.json()

        # Transformando asks em DataFrame
        df_asks = pd.DataFrame(data['asks'], columns=['price', 'volume'])
        df_asks['type'] = 'ask'

        # Transformando bids em DataFrame
        df_bids = pd.DataFrame(data['bids'], columns=['price', 'volume'])
        df_bids['type'] = 'bid'

        df_order_book = pd.concat([df_asks, df_bids], ignore_index=True)

        return df_order_book

    except Exception as e:
        print("❌ Erro ao consultar orderbook:", e)
        return None

def resumir_orderbook_df(df_orderbook, top_n=5):
    asks = df_orderbook[df_orderbook["type"] == "ask"].head(top_n)
    bids = df_orderbook[df_orderbook["type"] == "bid"].head(top_n)

    vol_asks = asks["volume"].astype(float).sum()
    vol_bids = bids["volume"].astype(float).sum()

    if vol_asks == 0:
        pressao = None
    else:
        pressao = vol_bids / vol_asks

    return {
        "volume_asks_top": round(float(vol_asks), 6),
        "volume_bids_top": round(float(vol_bids), 6),
        "pressao_compra": None if pressao is None else round(float(pressao), 3)
    }

def resumir_orderbook_ponderado(df_orderbook, preco_atual, top_n=10):
    df = df_orderbook.copy()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    asks = df[df["type"] == "ask"].head(top_n)
    bids = df[df["type"] == "bid"].head(top_n)

    # Evitar divisão por zero ou valores não numéricos em 'price'
    asks["peso"] = preco_atual / asks["price"].replace(0, np.nan) # replace 0 with NaN to avoid division by zero
    bids["peso"] = bids["price"] / preco_atual

    volume_asks_ponderado = (asks["volume"] * asks["peso"]).sum()
    volume_bids_ponderado = (bids["volume"] * bids["peso"]).sum()

    total = volume_asks_ponderado + volume_bids_ponderado

    return {
        "pressao_compra_ponderada": (
            volume_bids_ponderado / total if total > 0 else None
        )
    }
