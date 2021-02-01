# from datetime import datetime, timedelta

# # import matplotlib.pyplot as plt
# import mplfinance as mpf
# import pandas as pd
# from finta import TA

import work as wk


# def calcula_r_compra_venda(df_criado):
#     r_determina_operaca = df_criado["close"] - df_criado["ema_1200"] >=0
#     r_determina_operaca_1 = df_criado["close"] - df_criado["ema_300"] >= 0

#     r_determina_operaca_2 = df_criado["close"] - df_criado["ema_1200"] < 0
#     r_determina_operaca_3 = df_criado["close"] - df_criado["ema_300"] <  0


#     r_libera_compra = r_determina_operaca & r_determina_operaca_1
#     r_libera_venda = r_determina_operaca_2 &   r_determina_operaca_3
#     r_liberado_operacao = ~(~ r_libera_compra & ~ r_libera_venda)
#     return r_libera_compra, r_libera_venda, r_liberado_operacao
    
# def criando_bd():
#     df_criado = pd.read_csv("dados_get.csv")
#     df_criado["ema_30"] =  TA.EMA(df_criado, 30)
#     df_criado["ema_100"] =  TA.EMA(df_criado, 100)
#     df_criado["ema_300"] =  TA.EMA(df_criado, 400)
#     df_criado["ema_1200"] =  TA.EMA(df_criado, 1200)
#     saida_BB =  TA.BBANDS(df_criado)
#     df_criado["BB_UPPER"] =  saida_BB["BB_UPPER"]
#     df_criado["BB_LOWER"] =  saida_BB["BB_LOWER"]
#     df_criado["normaliza"] = df_criado["close"] - df_criado["ema_300"]
#     df_criado["r_compra"], df_criado["r_venda"], df_criado["libera_trade"] = calcula_r_compra_venda(df_criado)
#     df_criado.head()
#     return df_criado

# def test_primeiro_teste():
#     df_criado = criando_bd()
#     m1 = wk.Mercador(200, wk.estrategia)
#     g1 = wk.gerador_dados(df_criado)

#     m1.novo_tick(next(g1)[1])
#     m1.novo_tick(next(g1)[1])


def test_for_ganhando():
    m1 = wk.Mercador(100)

    #comprar 30
    m1.ajusta_portifolio_por(0.3,100)
    # vender 10
    m1.ajusta_portifolio_por(0.2,120)
    print(m1)

def test_for_perdendo():
    m1 = wk.Mercador(100)

    #comprar 30
    m1.ajusta_portifolio_por(0.3,120)
    # vender 10
    m1.ajusta_portifolio_por(0.2,100)
    print(m1)



# def test_for():
#     df_criado = criando_bd()
#     m1 = wk.Mercador(200, wk.estrategia)
#     g1 = wk.gerador_dados(df_criado)

#     for linha in g1:
#         m1.novo_tick(linha[1])


# test_for()

