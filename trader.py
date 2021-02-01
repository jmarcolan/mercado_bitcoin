
import negociacao as ng
import sqlite3

BD_PATH = "dados_varias_coin.db"
def constroi_bd_bot():
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS bot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin TEXT NOT NULL,
        qnt_brl_inicial REAL,
        qnt_coin REAL,
        qnt_brl REAL);
        """
    conn = sqlite3.connect(BD_PATH)
    c = conn.cursor()
    c.execute(create_table_sql)
    c.close()

def constroi_bd_bot_operacao():
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS dados_trade (
        tid_order INTEGER,
        # tid INTEGER,
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
    c.close()



class bot_trader:
    def __init__(self, id):
        self.lista_ordens_q_controla_aberta = []
        self.qnt_dinheiro = 100
        self.qnt_moeda_digital = 0
         
    
    def posiciona_ordem(self):
        pass

    def get_portifolio(self):
        pass

# resposta por criar
# "order": {
#             "order_id": 39180215,
#             "coin_pair": "BRLXRP",
#             "order_type": 1,
#             "status": 2,
#             "has_fills": false,
#             "quantity": "0.10000000",
#             "limit_price": "2.10100",
#             "executed_quantity": "0.00000000",
#             "executed_price_avg": "0.00000",  
#             "fee": "0.00000000",
#             "created_timestamp": "1612220970",
#             "updated_timestamp": "1612220970",
#             "operations": []
#         }

# resposta por terminar
# "order": {
#             "order_id": 39180215,
#             "coin_pair": "BRLXRP",
#             "order_type": 1,
#             "status": 3,
#             "has_fills": false, # nao foi preenchida
#             "quantity": "0.10000000",
#             "limit_price": "2.10100",
#             "executed_quantity": "0.00000000",
#             "executed_price_avg": "0.00000",
#             "fee": "0.00000000", # quantidade paga
#             "created_timestamp": "1612220970",
#             "updated_timestamp": "1612221038",
#             "operations": []
#         }