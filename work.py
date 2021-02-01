# btc = {"qnt_moeda": 1, "v_negociado":23423, "t_operaca": "buy!sell" }
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta
# import mplfinance as mpf
# from finta import TA
# def gerador_dados(df_criado):
#     for row in df_criado.iterrows():
#         yield row

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