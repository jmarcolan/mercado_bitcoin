import estrategias as es
import work as wk

def test_a():
    df_inicial = es.import_pandas_from_csv("saida_xrp.csv")
    m1 = wk.Mercador_back_test_grid(100, 0.05) #0.3 centavos
    df_criado = es.estrategia_grid(df_inicial, 0.05)
    m1 = es.back_test_grid(df_inicial, m1, df_criado)
    assert 1 == 1

test_a()