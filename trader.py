
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
        id INTEGER PRIMARY KEY AUTOINCREMENT
        order_id INTEGER,
        bot_id INTEGER,
        coin_pair TEXT,
        order_type INTEGER,
        status INTEGER,
        has_fills BOOL,
        quantity TEXT,
        limit_price TEXT,
        executed_quantity TEXT,
        executed_price_avg TEXT,  
        fee TEXT,
        created_timestamp TEXT,
        updated_timestamp TEXT
        );
        """
    conn = sqlite3.connect(BD_PATH)
    c = conn.cursor()
    c.execute(create_table_sql)
    c.close()



class bot_trader:
    def _inicializa_qnt_moeda_digital(self,id):
        r_existe_bot = False
        if r_existe_bot:
            return 0
        else:
            return 0

    def _inicializa_qnt_moeda_real(self, id):
        r_existe_bot = False
        if r_existe_bot:
            def get_bd_qnt_():
                pass


            return 0
        else:
            return 50
        
        
        return 100
    
    def __init__(self, id):
        self.lista_ordens_q_controla_aberta = ["200","300"]
        self.qnt_dinherio_atual = self._inicializa_qnt_moeda_real(id)
        self.qnt_moeda_digital = self._inicializa_qnt_moeda_digital(id)
    
    def _get_ja_possui_operacoes(self):
        return False

    def _atualiza_ordem_negociacao(self):
        pass

    def _create_ordem_negociacao(self):
        pass

    def _operacao_compra(self):
        r_possui_operacao_aberta = self._get_ja_possui_operacoes()

        if r_possui_operacao_aberta:
            self._atualiza_ordem_negociacao()
        else:
            self._create_ordem_negociacao()




    def _operacao_compra(self, porcentagem, valor_negociado, tempo):
        pass

    def _operacao_venda(self, porcentagem, valor_negociado, tempo):
        pass

    def _get_qnt_moeda_digital(self):
        return 100

    def _get_qnt_dinheiro_atual(self):
        return 0

    def ajusta_portifolio_por(self, por_para_ajustar, v_negociacao, tempo):
        def get_porcento_atual():
            self.qnt_moeda_digital = self._get_qnt_moeda_digital()
            self.qnt_dinherio_atual = self._get_qnt_dinheiro_atual()

            s = self.qnt_moeda_digital*v_negociacao * 100/(self.qnt_moeda_digital*v_negociacao + self.qnt_dinherio_atual) # so nao pode ser zero

            s =  s/100

            return s 
        



        por_atual = get_porcento_atual()
        r_oper_compra = por_para_ajustar >= por_atual
        r_oper_venda = por_para_ajustar < por_atual
        if r_oper_compra:
            ajuste = por_para_ajustar - por_atual
            # self._operacao_compra(ajuste , v_negociacao, tempo)
        if r_oper_venda:
            self._operacao_venda(por_atual - por_para_ajustar, v_negociacao, tempo)

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