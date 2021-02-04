
import negociacao as ng
import sqlite3
import negociacao as api_negociacao
import time
BD_PATH = "dados_varias_coin.db"
def constroi_bd_bot():
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS bot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin TEXT NOT NULL,
        qnt_brl_inicial REAL,
        qnt_coin REAL,
        qnt_brl_atual REAL,
        dis REAL
        );
        """
    conn = sqlite3.connect(BD_PATH)
    c = conn.cursor()
    c.execute(create_table_sql)
    c.close()

def constroi_bd_bot_operacao():
    # estado_ordem :candelada,"compra_aberta", "compra_criada", "compra_executada",venda_aberta", "venda_criada", "venda_executada", "finalizada"

    create_table_sql = """
        CREATE TABLE IF NOT EXISTS operacoes_bot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        bot_id INTEGER,
        estado_ordem TEXT,

        valor_compra TEXT,
        qnt_comprada TEXT,
        order_compra_id INTEGER,
        

        valor_venda TEXT,
        qnt_vendida TEXT,
        order_venda_id INTEGER,
        

        lucro TEXT,
        fee TEXT
        );
        """

    conn = sqlite3.connect(BD_PATH)
    c = conn.cursor()
    c.execute(create_table_sql)
    c.close()

def inicializa_bot(id, brl=100, distancia=0.06, pair="XRP"):
    def parse_bot(tupla):
        dic_saida ={
                "bot_id": tupla[0],
                "coin": tupla[1],
                "qnt_brl_inicial": tupla[2],
                "qnt_coin": tupla[3],
                "qnt_brl_atual": tupla[4],
                "distancia": tupla[5]
            }
        return dic_saida 


    def create_bot(brl,distancia, pair):
        conn = sqlite3.connect(BD_PATH)
        cur = conn.cursor()
        
        sql = f'INSERT INTO bot(coin, qnt_brl_inicial, qnt_coin, qnt_brl_atual, dis) VALUES(?,?,?,?,?)'
        data_tuple = (pair, brl, 0, brl, distancia)
        cur.execute(sql,data_tuple)
        conn.commit()
        conn.close()
    
    def r_get_bot(id):
        conn = sqlite3.connect(BD_PATH)
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM bot where id == {id}')
        rows = cur.fetchone()
        conn.close()
        r_existe_bot = rows != None
        
        if not r_existe_bot:
            return r_existe_bot, None
        else:
            return r_existe_bot, parse_bot(rows)

    r_existe_bot, bot = r_get_bot(id)

    if not r_existe_bot:
        create_bot(brl, distancia, pair)
        bot = inicializa_bot(id, brl, pair)
        return bot
    else:
        return bot

# constroi_bd_bot()

# print(inicializa_bot(5))

class Boot_dados:
    def __init__(self, dados_bot, qnt_trade):
        self.qnt_moeda_trade = qnt_trade
        self.dados_bot = dados_bot
        self._get_ordens()


    def _atualiza_bot(self):
        conn = sqlite3.connect(BD_PATH)
        cur = conn.cursor()
        sql_str = f"""UPDATE bot
        SET  qnt_brl_atual = {self.dados_bot['qnt_brl_atual']},
        qnt_coin = {self.dados_bot['qnt_coin']}
        WHERE id == {self.dados_bot['bot_id']}"""
        cur.execute(sql_str)
        conn.commit()
        conn.close()
        
        
    def _parse_ordens(self,elemento):
        # corrigir
        
        elemento = {
            "id_ordem": elemento[0],
            "bot_id": elemento[1],
            "estado_ordem": elemento[2],

            "valor_compra": float(elemento[3]),
            "qnt_comprada": float(elemento[4]), #arrumar
            "order_compra_id": elemento[5], #servidor vai passar
        

            "valor_venda": float(elemento[6]),
            "qnt_vendida": float(elemento[7]),
            "order_venda_id": elemento[8], #servidor vai passar
            "lucro": elemento[9],
            "fee": elemento[10]
           
        }
        return elemento

    def _get_ordens(self):
        conn = sqlite3.connect(BD_PATH)
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM operacoes_bot WHERE bot_id == {self.dados_bot["bot_id"]}  AND estado_ordem != "cancelada" AND estado_ordem != "finalizada";')
        rows = cur.fetchall()
        conn.close()
        self.ls_ordens = []
        for elemento in rows:
            self.ls_ordens.append(self._parse_ordens(elemento))
        

    


    def cria_ordens(self, valor_compra):
        def envia_ordem(e):
            conn = sqlite3.connect(BD_PATH)
            cur = conn.cursor()
            
            sql = f"""
            INSERT INTO operacoes_bot(bot_id, estado_ordem, valor_compra, qnt_comprada, valor_venda, qnt_vendida)
            VALUES(?,?,?,?,?,?)
            """
            data_tuple = (e["bot_id"], e["estado_ordem"],
            e["valor_compra"], e["qnt_comprada"], 
            e["valor_venda"], e["qnt_vendida"])
            cur.execute(sql,data_tuple)
            conn.commit()
            conn.close()


        elemento = {
            "bot_id": self.dados_bot["bot_id"],
            "estado_ordem": "compra_aberta",

            "valor_compra": str(valor_compra),
            "qnt_comprada": str(self.qnt_moeda_trade), #arrumar
            # order_compra_id INTEGER, #servidor vai passar
        

            "valor_venda": str(valor_compra + self.dados_bot["distancia"]),
            "qnt_vendida": str(self.qnt_moeda_trade ),
            # order_venda_id INTEGER, #servidor vai passar
        }

        envia_ordem(elemento)
        self._get_ordens() # sempre atualizar a lista, ta batendo no sql ao tem problema

    def cancela_ordens(self, ls_id_cancelar):

        def envia_ordem_cancelar(id_cancelado):
            conn = sqlite3.connect(BD_PATH)
            cur = conn.cursor()
            sql_str = """UPDATE operacoes_bot
            SET estado_ordem = 'cancelada'
            WHERE id == ?"""

            cur.execute(sql_str, (id_cancelado, ))
            conn.commit()
            conn.close()
        
        for id_cancelado in ls_id_cancelar:
            envia_ordem_cancelar(id_cancelado)
        self._get_ordens()
    

    def _update_ordem_banco_dados(self, elemento, resposta):
        order_id = resposta["order_id"]
        status = resposta["status"] # 2 opem, 3 cancelada, 4 filled
        quantidade_moeda = resposta["fee"]
        valor = resposta["executed_price_avg"]

    def atualiza_ordens(self):
        self._get_ordens()

        ## UUMA DAS FUNCOES MAIS IMPORTANTES
        def cria_funca_resposta(e):
            def resposta_compra(recebe_resposta):
                r_criou_operacao = recebe_resposta["status_code"] == 100
                if r_criou_operacao:
                    ordem = recebe_resposta["response_data"]["order"]
                    r_aberta = ordem["status"] == 2
                    r_completada = ordem["status"] == 4
                    r_ja_comprada = e["estado_ordem"] == "compra_criada"

                    if r_aberta and not r_ja_comprada:
                        def atualiza_banco_dados(elemento, ordem):
                            conn = sqlite3.connect(BD_PATH)
                            cur = conn.cursor()
                            sql_str = f"""UPDATE operacoes_bot
                            SET estado_ordem = 'compra_criada',
                            order_compra_id = '{ordem['order_id']}'
                            WHERE id == {elemento["id_ordem"]}"""

                            cur.execute(sql_str)
                            conn.commit()
                            conn.close()
                    
                        atualiza_banco_dados(e,ordem)
                    
                    if r_completada:
                        def atualiza_banco_dados(elemento, ordem):
                            valor_compra = float(ordem['executed_price_avg'])
                            qnt_comprada = float(ordem['executed_quantity']) - float(ordem['fee'])
                            conn = sqlite3.connect(BD_PATH)
                            cur = conn.cursor()
                            sql_str = f"""UPDATE operacoes_bot
                            SET estado_ordem = 'compra_executada',
                            order_compra_id = {ordem['order_id']},
                            valor_compra = '{str(valor_compra)}',
                            qnt_comprada = '{str(qnt_comprada)}' 
                            WHERE id == {elemento['id_ordem']}"""
                            cur.execute(sql_str)
                            conn.commit()
                            conn.close()

                            self.dados_bot["qnt_brl_atual"]=  self.dados_bot["qnt_brl_atual"] - (qnt_comprada *valor_compra)
                            self.dados_bot["qnt_coin"]=  self.dados_bot["qnt_coin"] + qnt_comprada 
                    
                        atualiza_banco_dados(e,ordem)
            return resposta_compra

        def cria_compra(e):
            pair = self.dados_bot["coin"]
            valor     = e["valor_compra"]
            qnt_moeda = e["qnt_comprada"]
            r_existe_dinheiro = self.dados_bot["qnt_brl_atual"] > valor*qnt_moeda
            
            def get_livro(recebe_livo_resposta):
                r_livro = recebe_livo_resposta["status_code"] == 100
                if r_livro:
                    melhor_valor_compra = float(recebe_livo_resposta["response_data"]["orderbook"]["bids"][0]["limit_price"])
                    melhor_valor_venda = float(recebe_livo_resposta["response_data"]["orderbook"]["asks"][0]["limit_price"])
                    espread =  melhor_valor_venda - melhor_valor_compra
                    bom_valor_book = melhor_valor_compra + espread * 0.2
                    r_melhor_valor_book = bom_valor_book < valor
                    if r_melhor_valor_book:
                        e["valor_compra"] = bom_valor_book
                    
                    api_negociacao.place_buy_order(str(e["valor_compra"]), str(qnt_moeda), pair, cria_funca_resposta(e))

                        
                        
            api_negociacao.list_orderbook(pair, get_livro)


        ls_compra_aberta_pelo_bot = list(
            map(cria_compra,
            filter(lambda x: x["estado_ordem"] == "compra_aberta",
            self.ls_ordens )))

            
        def create_funcao_venda(e):
            def resposta_venda(recebe_resposta):
                r_criou_operacao = recebe_resposta["status_code"] == 100
                if r_criou_operacao:
                    ordem = recebe_resposta["response_data"]["order"]
                    r_aberta = ordem["status"] == 2
                    r_completada = ordem["status"] == 4
                    r_ja_comprada = e["estado_ordem"] == "venda_criada"


                    if r_aberta and not r_ja_comprada:
                        def atualiza_banco_dados(elemento, ordem):
                            conn = sqlite3.connect(BD_PATH)
                            cur = conn.cursor()
                            sql_str = f"""UPDATE operacoes_bot
                            SET estado_ordem = 'venda_criada',
                            order_venda_id = '{ordem['order_id']}'
                            WHERE id == {elemento["id_ordem"]}"""

                            cur.execute(sql_str)
                            conn.commit()
                            conn.close()
                    
                        atualiza_banco_dados(e,ordem)
                    
                    if r_completada:
                        def atualiza_banco_dados(elemento, ordem):
                            valor_venda = float(ordem['executed_price_avg']) - float(ordem['fee'])
                            qnt_venda = float(ordem['executed_quantity'])
                            conn = sqlite3.connect(BD_PATH)
                            cur = conn.cursor()
                            sql_str = f"""UPDATE operacoes_bot
                            SET estado_ordem = 'venda_executada',
                            order_venda_id = {ordem['order_id']},
                            valor_venda = '{str(valor_venda)}',
                            qnt_vendida = '{str(qnt_venda)}' 
                            WHERE id == {elemento['id_ordem']}"""
                            cur.execute(sql_str)
                            conn.commit()
                            conn.close()

                            self.dados_bot["qnt_brl_atual"]=  self.dados_bot["qnt_brl_atual"] + (valor_venda * qnt_venda)
                            self.dados_bot["qnt_coin"]=  self.dados_bot["qnt_coin"] - qnt_venda
                        
                        atualiza_banco_dados(e,ordem)
            return resposta_venda



        def get_se_executada(e):
            api_negociacao.get_order(e["order_compra_id"], self.dados_bot["coin"], create_funcao_venda(e) )
        

        ls_compra_criada = list(map(get_se_executada,
            filter(lambda x: x["estado_ordem"] == "compra_criada", 
            self.ls_ordens )))


        # estado_ordem :candelada,"compra_aberta", "compra_criada", "compra_executada",venda_aberta", "venda_criada", "venda_executada", "finalizada"
        def cria_venda(e):
            # se a compra foi executada abrir uma venda isso é no sql
            def update_banco_dados(e):
                conn = sqlite3.connect(BD_PATH)
                cur = conn.cursor()
                sql_str = f"""UPDATE operacoes_bot
                SET estado_ordem = 'venda_aberta',
                "valor_venda"= '{str(e['valor_compra'] + self.dados_bot["distancia"])}',
                "qnt_vendida"= '{e['qnt_comprada']}'
                WHERE id == {e["id_ordem"]}"""

                cur.execute(sql_str)
                conn.commit()
                conn.close()
            # se aberta uma venda abrir uma ordem de venda no mercado,
            update_banco_dados(e)

        
        ls_compra_executada = list(map(cria_venda,
            filter(lambda x: x["estado_ordem"] == "compra_executada", 
            self.ls_ordens )))
        
        



        def get_venda_aberta(e):
            # se ta liberado para venda abrir uma ordem no mercado bitcoin
            valor     = e["valor_venda"]
            qnt_moeda = e["qnt_vendida"]
            r_existe_dinheiro = self.dados_bot["qnt_brl_atual"] > valor*qnt_moeda
            pair = self.dados_bot["coin"]
   
            api_negociacao.place_sell_order(str(valor), str(qnt_moeda), pair, create_funcao_venda(e))


        ls_venda_aberta = list(map(get_venda_aberta,
            filter(lambda x: x["estado_ordem"] == "venda_aberta", 
            self.ls_ordens )))

        def get_venda_foi_executada(e):
            # caso abra uma ordem de venda esperar
            api_negociacao.get_order(e["order_venda_id"], self.dados_bot["coin"], create_funcao_venda(e) )
            
        ls_venda_criada = list(map(get_venda_foi_executada,
            filter(lambda x: x["estado_ordem"] == "venda_criada", 
            self.ls_ordens )))

        def finaliza(e):
            # gestão do banco de dados para finalizar a operação ($profit)
            conn = sqlite3.connect(BD_PATH)
            cur = conn.cursor()
            sql_str = f"""UPDATE operacoes_bot
            SET estado_ordem = 'finalizada'
            WHERE id == {e['id_ordem']}"""
            cur.execute(sql_str)
            conn.commit()
            conn.close()
        
        
        ls_venda_executada = list(map(finaliza,
        filter(
            lambda x: x["estado_ordem"] == "venda_executada", 
            self.ls_ordens )))
        
        self._atualiza_bot()



if __name__ == "__main__":
    constroi_bd_bot()
    constroi_bd_bot_operacao()
    
    bot = inicializa_bot(4,20)
    bd = Boot_dados(bot, 0.11)
    # bd.cria_ordens(2.09)
    bd.atualiza_ordens()
    print(bd.dados_bot)