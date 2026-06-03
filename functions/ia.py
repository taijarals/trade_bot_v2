
# ==============================================================
# 🧠 INTELIGÊNCIA ARTIFICIAL
# ==============================================================

def montar_prompt_ia(contexto):
    prompt = f"""
Você é um analista quantitativo especializado em mercado financeiro,
microestrutura e fluxo de ordens.

Avalie o estado atual do mercado e decida a melhor ação entre:
COMPRAR, VENDER ou ESPERAR.

Contexto atual do mercado:

Ativo: {contexto['ativo']}
Timeframe: {contexto['timeframe']}

Preço atual: {contexto['preco_atual']}
Retorno curto (%): {contexto['retorno_curto_pct']}
Volatilidade (%): {contexto['volatilidade_pct']}
Tendência curta: {contexto['tendencia_curta']}

Variação 24h (%): {contexto['variacao_24h_pct']}
Máxima 24h: {contexto['max_24h']}
Mínima 24h: {contexto['min_24h']}
Volume 24h: {contexto['volume_24h']}
Trades 24h: {contexto['trades_24h']}

Spread (%): {contexto['spread_pct']}

Order Book:
- Volume bids (top): {contexto['volume_bids_top']}
- Volume asks (top): {contexto['volume_asks_top']}
- Bid/Ask ratio: {contexto['bid_ask_ratio_top']}
- Pressão de compra: {contexto['pressao_compra']}
- Pressão de compra ponderada: {contexto['pressao_compra_ponderada']}

Responda exclusivamente no formato JSON abaixo:

{{
  "acao": "COMPRAR | VENDER | ESPERAR",
  "confianca": 0.0,
  "justificativa_curta": ""
}}
"""
    return prompt

def analisar_mercado(contexto_mercado, client):
    prompt_final = montar_prompt_ia(contexto_mercado)

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-v4-flash:free",
            messages=[
                {"role": "user", "content": prompt_final}
            ],
            max_tokens=300,
            temperature=0.2
        )

        if response and response.choices and response.choices[0].message:
            return response.choices[0].message.content
        else:
            # Log the full response object for debugging if choices are missing
            print(f"❌ API response did not contain expected choices or message: {response}")
            return json.dumps({"acao": "ESPERAR", "confianca": 0.0, "justificativa_curta": "API response missing choices or message."})
    except Exception as e:
        print(f"❌ Erro ao chamar a API da IA: {e}")
        return json.dumps({"acao": "ESPERAR", "confianca": 0.0, "justificativa_curta": f"Erro na chamada da API da IA: {e}"})
