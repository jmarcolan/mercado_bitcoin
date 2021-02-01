# btc = {"qnt_moeda": 1, "v_negociado":23423, "t_operaca": "buy!sell" }
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta
# import mplfinance as mpf
# from finta import TA
# def gerador_dados(df_criado):
#     for row in df_criado.iterrows():
#         yield row

# def estrategia(linha_tabela):
#     def saida_proporção_conta_compra(x_sai):
#         pro = ( 13000 - x_sai) * 80/(26000) + 10 

#         pro = pro/100

#         r_saturo_positivo = pro > 0.9
#         r_saturo_negativo = pro < 0.1
#         if r_saturo_positivo:
#             return 90/100
#         if r_saturo_negativo:
#             return 10/100
#         return pro

#     def saida_proporção_conta_venda(x_sai):
#         pro = (x_sai-13000) * (10 - 90)/(13000 + 13000)
#         pro = pro/100

#         r_saturo_positivo = pro > 0.9
#         r_saturo_negativo = pro < 0.1
#         if r_saturo_positivo:
#             return 90/100
#         if r_saturo_negativo:
#             return 10/100
#         return pro
    
    
#     r_compra = linha_tabela["r_compra"]  
#     r_venda = linha_tabela["r_venda"]
#     r_libera = linha_tabela["libera_trade"]
    
#     if r_libera:
#         if r_compra:
#             return 0, saida_proporção_conta_compra(linha_tabela["normaliza"])
#         if r_venda:
#             return 1, saida_proporção_conta_venda(linha_tabela["normaliza"])
#     else:
#         return 2, 0




# class Mercador():
#     def __init__(self, quantidade_inicial, estrategia):
#         self.quantidade_inicial = quantidade_inicial
#         self.quantidade_atual = quantidade_inicial
#         self.btc_comprados_atual = []
#         self.estrategia = estrategia
        
        

#     def novo_tick(self, linha_tabela):
#         estado, qnt_bitcoin_ideal = self.estrategia(linha_tabela)
        
#         r_compra = estado == 0
#         r_venda = estado == 1
#         r_incerto = estado == 2
#         if not r_incerto:
#             if r_compra:
#                 self._fazer_operacao_compra(qnt_bitcoin_ideal, linha_tabela["close"])
                
            
#             if r_venda:
#                 self._fazer_operacao_compra(qnt_bitcoin_ideal, linha_tabela["close"])
                
#             print(self.btc_comprados_atual)
#             print(self.quantidade_atual)
        
#     def _get_quantidade(self):
#         def map_qnt_btc(x):
#             return x["qnt_moeda"]
        
#         ls_me_com = list(map(map_qnt_btc,self.btc_comprados_atual))
#         r_possui_valore = len(ls_me_com)
#         if r_possui_valore:
#             soma = pd.Series(ls_me_com).sum()
#             return soma
#         else:
#             return 0
    
    

#     def _get_preco_medio_por(self):
#         def map_qnt_btc(x):
#             return x["qnt_moeda"] * x["v_negociado"]
        
#         def get_porcento(soma_btc):
#             s = soma_btc * 100/(soma_btc + self.quantidade_atual) # so nao pode ser zero
#             return s 
        
#         ls_me_com = list(map(map_qnt_btc, self.btc_comprados_atual))
#         r_possui_valore = len(ls_me_com)
#         if r_possui_valore:
            
#             soma_btc = pd.Series(ls_me_com).sum()
#             soma_btc_p =  get_porcento(soma_btc)
#             return soma_btc_p
#         else:
#             return 0

#     def _get_fez_compra(self, preco):
#         def fil_compra(x):
#             r_fez_compra =  preco > x["v_negociado"]*(1+ 1/100) and preco < x["v_negociado"]*-(1+ 1/100)
            
#             return r_fez_compra
        
#         r_ja_fez_uma_compra = len(list(filter(fil_compra, self.btc_comprados_atual))) != 0
#         return r_ja_fez_uma_compra
    
#     def _realizar_compra(self, qnt_compra, preco_tick):
#         qnt_compra_2 = qnt_compra
#         qnt_compra_brl  = self.quantidade_atual * qnt_compra_2
#         qnt_compra_pedida_moeda = qnt_compra_brl/preco_tick
        
#         self.quantidade_atual = self.quantidade_atual - qnt_compra_brl
        
        
#         self.btc_comprados_atual.append({"qnt_moeda": qnt_compra_pedida_moeda, 
#                                          "v_negociado":preco_tick,
#                                          "t_operaca": "buy" })
        
        
        
#     def _realizar_venda(self, qnt_venda, preco_tick):
#         def map_valores(x):
#             return preco_tick - x["v_negociado"] 
        
#         saida = list(map(map_valores, self.btc_comprados_atual))

#         get_inde_maior = saida.index(max(saida))
#         operacao_aberta = self.btc_comprados_atual[get_inde_maior]
        
#         r_possui_qnt_vender = operacao_aberta["qnt_moeda"] > qnt_venda/preco_tick
#         if r_possui_qnt_vender:
#             self.quantidade_atual = self.quantidade_atual + qnt_venda * preco_tick
#             operacao_aberta["qnt_moeda"] = operacao_aberta["qnt_moeda"] - qnt_venda
            
#         else:
#             self.quantidade_atual = self.quantidade_atual + qnt_venda * preco_tick
#             self.btc_comprados_atual.pop(get_inde_maior)
#             print("_-------------------------------")
#             print(operacao_aberta)
        
    
    
#     def _fazer_operacao_compra(self, qnt_bitcoin_ideal, preco_tick ):
#         qnt_bitcoin_por = self._get_preco_medio_por()
        
#         r_comprar_mais = qnt_bitcoin_por < qnt_bitcoin_ideal
#         r_vender_mais = qnt_bitcoin_por >= qnt_bitcoin_ideal
       
#         if r_comprar_mais:
#             r_ja_fez_uma_compra = self._get_fez_compra(preco_tick)
#             if not r_ja_fez_uma_compra:
#                 self._realizar_compra(qnt_bitcoin_ideal - qnt_bitcoin_por, preco_tick)
                    
#         if r_vender_mais:
#             r_ja_fez_uma_compra = self._get_fez_compra(preco_tick)
#             if not r_ja_fez_uma_compra:
#                 self._realizar_venda(qnt_bitcoin_por - qnt_bitcoin_ideal ,preco_tick)
        

class Mercador():
    def __init__(self, qnt_dinheiro):
        self.qnt_dinherio_inicial = qnt_dinheiro
        self.qnt_dinherio_atual = qnt_dinheiro
        self.btc_atual = 0
        self.ls_valor_carteira = []
        self.ls_tipo = []
        self.ls_tempo = []
        self.ls_dict= [] 

    def _get_taxa(self):
        return 1 - 0.7/100
        
    def _operacao_compra(self, por_para_ajustar, v_negociacao, tempo):
        btc_compra = (self.qnt_dinherio_atual * por_para_ajustar) / v_negociacao
        self.btc_atual = self.btc_atual + (btc_compra * self._get_taxa())
        self.qnt_dinherio_atual = self.qnt_dinherio_atual -  (self.qnt_dinherio_atual * por_para_ajustar)
        self.ls_valor_carteira.append(self.qnt_dinherio_atual + self.btc_atual*v_negociacao )
        self.ls_tipo.append("compra")
        self.ls_tempo.append(tempo)

        self.ls_dict.append({"tipo":"compra", 
                            "tempo":tempo, 
                            "qnt_btc": btc_compra})
    
    

    def _operacao_venda(self, por_para_ajustar, v_negociacao, tempo):
        btc_venda = self.btc_atual * por_para_ajustar
        self.btc_atual = self.btc_atual - btc_venda

        self.qnt_dinherio_atual = self.qnt_dinherio_atual + (btc_venda* v_negociacao * self._get_taxa())
        self.ls_valor_carteira.append(self.qnt_dinherio_atual + self.btc_atual*v_negociacao )
        self.ls_tipo.append("venda")
        self.ls_tempo.append(tempo)

        self.ls_dict.append({"tipo":"venda", 
                            "tempo":tempo, 
                            "qnt_btc": btc_venda})



    def ajusta_portifolio_por(self, por_para_ajustar, v_negociacao, tempo):
        def get_porcento_atual():
            s = self.btc_atual*v_negociacao * 100/(self.btc_atual*v_negociacao + self.qnt_dinherio_atual) # so nao pode ser zero

            s =  s/100

            return s 
        
        r_oper_compra = por_para_ajustar >= get_porcento_atual()
        r_oper_venda = por_para_ajustar < get_porcento_atual()
        if r_oper_compra:
            self._operacao_compra(por_para_ajustar - get_porcento_atual(), v_negociacao, tempo)
        if r_oper_venda:
            self._operacao_venda(get_porcento_atual() - por_para_ajustar, v_negociacao, tempo)