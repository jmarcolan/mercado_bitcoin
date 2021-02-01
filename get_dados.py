import urllib3
import sqlite3
import json


import sys

iMaxStackSize = 10000
sys.setrecursionlimit(iMaxStackSize)

# {

    # "tid": 8190628, #numero da negociação
#     "date": 1611851116,
#     "type": "sell",
#     "price": 172100.06009,
#     "amount": 0.00068632
# },


BD_PATH = "dados_varias_coin.db"

def constroi_bd():
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS dados_trade (
        tid INTEGER,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin TEXT NOT NULL,
        date INTEGER NOT NULL,
        type TEXT NOT NULL,
        price REAL,
        amount REAL);
        """
    conn = sqlite3.connect(BD_PATH)
    c = conn.cursor()
    c.execute(create_table_sql)



def testa_recebidos(coin):
    conn = sqlite3.connect(BD_PATH)
    query = f'SELECT * FROM dados_trade WHERE coin =="{coin}"'
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for record in rows:
        print(record)


def envia_record_sem_testar_multiplos(l_records, coin):
    def map_varios(re):
       data_tuple= (re["tid"], re["date"],re["type"], re["price"], re["amount"],coin)
       return data_tuple

    sql = f'INSERT INTO dados_trade(tid,date,type,price,amount,coin) VALUES(?,?,?,?,?,?)'

    ls_tuplas = list(map(map_varios, l_records))

    # data_tuple = (re["tid"], re["date"],re["type"], re["price"], re["amount"])
    conn = sqlite3.connect(BD_PATH)
    cur = conn.cursor()
    cur.executemany(sql, ls_tuplas)
    conn.commit()
    conn.close()



def envia_record(conn, re, coin):
    def tes_exist_record(conn, record):
        query = f'SELECT * FROM dados_trade WHERE tid={record["tid"]} AND coin=="{coin}"'
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()

        r_tem_daos = len(list(rows)) >= 1
        return r_tem_daos

    r_existe_record = tes_exist_record(conn, re)
    if not r_existe_record:
        sql = f'INSERT INTO dados_trade(tid,date,type,price,amount, coin) VALUES(?,?,?,?,?,?)'


        data_tuple = (re["tid"], re["date"],re["type"], re["price"], re["amount"], coin)
        cur = conn.cursor()
        cur.execute(sql,data_tuple)
        conn.commit()
        conn.close()
        # print("adicionado dado", re["tid"])
        return True
    else:
        conn.close()
        # print("dados ja existentes", re["tid"])
        return False

def grava_dados(l_records, coin):
    
    envia_record_sem_testar_multiplos(l_records, coin)
    # for record in l_records:
    #     envia_record(conn, record)

def get_dados_trades(moeda="BTC", tid=0, since=0):
    http = urllib3.PoolManager()
    
    
    r_pegar_passados_tid = int(tid) != 0
    r_pegar_passados_sin = int(since) != 0
    r_pegar_atual = ((not r_pegar_passados_tid) and (not r_pegar_passados_sin))

    if r_pegar_atual:
        r = http.request('GET', f'https://www.mercadobitcoin.net/api/{moeda}/trades/')
    elif r_pegar_passados_tid:
        r = http.request('GET', f'https://www.mercadobitcoin.net/api/{moeda}/trades/?tid={tid}')
    elif r_pegar_passados_sin:
        r = http.request('GET', f'https://www.mercadobitcoin.net/api/{moeda}/trades/{since}/')

    r_retornou_dados = r.status == 200
    if r_retornou_dados:
        return json.loads(r.data)
    else:
        return []


        

def get_ultimo_gravado(coin):
    query = f'SELECT * FROM dados_trade WHERE tid = (SELECT MAX(tid) FROM dados_trade WHERE coin=="{coin}") AND coin=="{coin}"'
    conn = sqlite3.connect(BD_PATH)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows[0]


def get_primeiro_gravado(coin):
    query = f'SELECT * FROM dados_trade WHERE tid = (SELECT MIN(tid) FROM dados_trade) AND coin=="{coin}'
    conn = sqlite3.connect(BD_PATH)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows[0]

def atualiza_ultimo_criado(coin):
    def get_ultimo_serivor(coin):
        l_records = get_dados_trades(coin)
        return  l_records[len(l_records)-1] 

    ultimo_gravado = get_ultimo_gravado(coin)
    ultimo_servidor = get_ultimo_serivor(coin)

    r_exist_dados_disponiveis = int(ultimo_servidor["tid"]) > int(ultimo_gravado[0])

    print(f'o ultimo gravado foi:{int(ultimo_gravado[0])} e ja estamos no {int(ultimo_servidor["tid"])} do {coin}')
    if r_exist_dados_disponiveis:
        def constroi_filter_tid(tid):
            def filtro_tid(x):
                r_atualizar = int(x["tid"]) >= tid
                return r_atualizar
            return filtro_tid


        l_records_gravar = get_dados_trades(coin, tid= ultimo_gravado[0])
        l_records_gravar_mini = list(filter(constroi_filter_tid(ultimo_gravado[0]), l_records_gravar))
        
        grava_dados(l_records_gravar_mini, coin)
        atualiza_ultimo_criado(coin)
        return True
    else:
        print("dados up to date")
        return False


# def get_dados_passados_aos_possuidos():
#     # 1577836800 inicio do ano
#     def get_primeiro(since_1):
#         l_records = get_dados_trades(since=since_1)
#         return  l_records[0] 


#     primeiro_servidor = get_primeiro("1577836800")
#     primeiro_gravado = get_primeiro_gravado()


#     r_exist_gap = int(primeiro_servidor["tid"]) < int(primeiro_gravado[0])

#     print(f'o primeiro gravado foi:{int(primeiro_gravado[0])} e no serivord no {int(primeiro_servidor["tid"])}')
#     if r_exist_gap:
#         l_records_gravar = get_dados_trades(tid=primeiro_servidor["tid"])
#         grava_dados(l_records_gravar)
#         get_dados_passados_aos_possuidos()

#     else:
#         print("Dados atualizados")
#         return False

def grava_dados_since(since, coin):
    primeiro_servidor = get_dados_trades(coin, since=since)
    grava_dados(primeiro_servidor,coin)
    atualiza_ultimo_criado(coin)


def starta_banco_de_dados(coin):
    constroi_bd()
    # pegar de hj 1577836800
    since= "1577836800" #"1612137600"
    grava_dados_since(since, coin)


if __name__ == "__main__":

    starta_banco_de_dados("BTC")
    starta_banco_de_dados("XRP")
    starta_banco_de_dados("LTC")
    # atualiza_ultimo_criado(coin)
# atualiza_ultimo_criado()
# if __name__ == "__main__":
#     print("oi mundo")
#     constroi_bd()
#     l_records = get_dados_trades()
#     grava_dados(l_records)