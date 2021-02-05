import work as wk
import pandas as pd
from datetime import datetime, timedelta

import numpy as np

import parse_dados_banco as pbd


def import_pandas_from_csv(path):
    def map_strin_date(x):
        return datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        
    df_criado = pd.read_csv(path)
    df_criado["date"] = df_criado["date"].map(map_strin_date)
    df_criado.set_index('date', inplace=True)
    return df_criado


def constroi_grid_estatico(valor_base, variacao_grid, valor_maximo=100):
    def aciona_valor(valor_atual):
        
        r_dentro_do_range = valor_atual < valor_maximo

        variacao_preco = valor_atual - valor_base
        r_gatilho_constori_nova_operacao = (variacao_preco % variacao_grid >= 0) & (variacao_preco % variacao_grid <= 0.00001)
        r_saida = r_gatilho_constori_nova_operacao and r_dentro_do_range
        return r_saida
    return aciona_valor

def estrategia_grid(df_inicial, grid_valor, valor_base=1, valor_maximo=100):
    df_criado = df_inicial.copy()
    map_valor_aciona_operacao = constroi_grid_estatico(valor_base, grid_valor, valor_maximo)
    df_criado["aciona"] = df_criado["close"].map(map_valor_aciona_operacao)
    return df_criado

def gerador_dados(df_criado):
    for row in df_criado.iterrows():
        yield row


# Primeira estratégia live.
def faz_estrategia_live(grid_valor, coin):
    db_candl = pbd.get_ultimo_candle_from_db(coin)
    df_estrategia = estrategia_grid(db_candl,grid_valor)
    r_aciona = df_estrategia.iloc[-1]["aciona"]
    v_close = df_estrategia.iloc[-1]["close"]
    return r_aciona, v_close





def range_do_valor(valor, limite_inferior, limite_superior, variacao):
    def get_range( limite_inferior, limite_superior, variacao):
        range_superior = np.arange(limite_inferior, limite_superior, variacao)
        range_inferior = np.arange(limite_inferior-variacao, limite_superior-variacao,variacao)
        range_bot = zip(range_superior,range_inferior)
        return range_bot

    range_bot = get_range(limite_inferior,limite_superior,variacao)
    for rang_sup, range_inf in range_bot:
        r_e_o_range = valor>range_inf and valor< rang_sup
        if r_e_o_range:
            rs_i = range_inf
            rs_s = rang_sup
            break
    return round(range_inf,8), round(rang_sup,8)


def faz_estrategia_live_aprimorada(limite_inferior, limite_superior, grid_valor, coin):
    # estrategia de grid para abrir as ordens de compra quando o candle tiver no range.
    db_candl = pbd.get_ultimo_candle_from_db(coin)
    v_close = db_candl.iloc[-1]["close"]
    v_limite_inf, v_limite_sup = range_do_valor(v_close,limite_inferior,limite_superior,grid_valor)
    return v_limite_inf, v_limite_sup, v_close





def back_test_grid(df_inicial, m1, df_estrategia):

    df_criado = df_estrategia
    g1 = gerador_dados(df_criado)
    
    
    for tempo, linha in g1:
    #     tempo, linha = next(g1)
        r_aciona = linha["aciona"]

        if r_aciona:
            m1.cria_ordens(linha["close"])
        
        m1.executa_ordens(linha["close"])

    return m1


if __name__ == "__main__":
    r_aciona,v_close = faz_estrategia_live(0.06,"XRP")
    print(r_aciona,v_close)
