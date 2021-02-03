import work as wk
import pandas as pd
from datetime import datetime, timedelta

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