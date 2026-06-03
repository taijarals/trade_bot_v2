
def pressao_bid_ask_df(df_ticker):
    last = df_ticker.iloc[-1]

    bid_vol = float(last["best.bid.volume"])
    ask_vol = float(last["best.ask.volume"])

    if ask_vol == 0:
        razao = None
    else:
        razao = bid_vol / ask_vol

    return {
        "bid_ask_ratio_top": None if razao is None else round(razao, 3)
    }


def montar_contexto_mercado(df_candles, df_ticker, df_orderbook):
    contexto = {}

    contexto.update(resumir_candles(df_candles))
    contexto.update(resumir_ticker_df(df_ticker))
    contexto.update(pressao_bid_ask_df(df_ticker))
    contexto.update(resumir_orderbook_df(df_orderbook))
    # Check if 'preco_atual' exists before calling resumir_orderbook_ponderado
    if "preco_atual" in contexto:
        contexto.update(resumir_orderbook_ponderado(df_orderbook, contexto["preco_atual"])) # Pass preco_atual
    else:
        print("""⚠️ 'preco_atual' not found in context. Cannot calculate 'pressao_compra_ponderada'.""")

    contexto["ativo"] = "BTC/BRL"
    contexto["timeframe"] = "1m"

    return contexto