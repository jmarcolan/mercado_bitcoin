import sqlite3
import pandas as pd
import datetime
import get_dados as api_dados

BD_PATH = "dados_varias_coin.db"
def pega_dados_since_db(tempo_passado, coin='XRP', BD_PATH = "dados_varias_coin.db"):
    
    datetime_object = datetime.datetime.now() - datetime.timedelta(minutes=tempo_passado)
    tm_ini = int(datetime_object.timestamp())
    con = sqlite3.connect(BD_PATH)

    df = pd.read_sql_query(f'SELECT * from dados_trade WHERE date >= {tm_ini} AND coin=="{coin}";', con)
    if not df.empty:
        df["Date"] =df['date'].map(datetime.datetime.fromtimestamp)

        r_existe_dados = len(df) !=0 
        if r_existe_dados:
            df_open = gera_pandas(df)
            df_open.set_index('date', inplace=True)
            return r_existe_dados, df_open
        else:
            print("deu pau e nao tem os dados")
            return r_existe_dados, None
    else:
        print("Banco de dados vazio")
        return False, None


def gera_pandas(df):
    def filter_dic_vaziu(dict_gerado):
        r_dict_vaziu = not bool(dict_gerado)
        return not r_dict_vaziu

    index, index_shift = gera_index_candle(df)
    index_g = zip(index, index_shift)

    ls_candle = []
    for t in index_g:
        ls_candle.append(calcula_candle(df, t[0], t[1]))
        
    ls_saida = list(filter(filter_dic_vaziu, ls_candle))
    df_saida = pd.DataFrame(ls_saida)
    return df_saida


def gera_index_candle(df, timer=5):
    d_start = df["Date"].iloc[0]
    d_fim = df["Date"].iloc[-1]
    
    d_start_shift = d_start +  datetime.timedelta(minutes=timer)
    d_fim_shift = d_fim +  datetime.timedelta(minutes=timer) 
    
    index = pd.date_range(start=d_start, end=d_fim, freq=f'{timer}min')
    index_shift = pd.date_range(start=d_start_shift, end=d_fim_shift, freq=f'{timer}min')
    return index, index_shift


def calcula_candle(df, d_inicio, d_fim):
    r_inicio= df["Date"] > d_inicio
    r_fim = df["Date"] < d_fim

    df_candle = df[(r_inicio & r_fim)]
    r_encontrou = len(df_candle) != 0
    if r_encontrou:
        candle= {}
        candle["date"] = d_inicio
        candle["fim"] = d_fim
        candle["open"] = df_candle["price"].iloc[0]
        candle["close"] = df_candle["price"].iloc[-1]
        candle["volume"] = df_candle["amount"].sum()
        candle["high"]= df_candle["price"].max()
        candle["low"] = df_candle["price"].min()
        return candle
    else:
        return {}


def get_ultimo_candle_from_db(coin="XRP", tempo=5):
    api_dados.atualiza_ultimo_criado(coin)
    r_existe_dados, df_open = pega_dados_since_db(5, coin)
    # .iloc[-1]["close"]
    return df_open
    

if __name__ == "__main__":
    df_candle = get_ultimo_candle_from_db("XRP")
    df_candle.head()