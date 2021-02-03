# class Mercador_back_teste:
#     def __init__(self, qnt_dinheiro):
#         self.qnt_dinherio_inicial = qnt_dinheiro
#         self.qnt_dinherio_atual = qnt_dinheiro
#         self.btc_atual = 0
#         self.ls_valor_carteira = []
#         self.ls_tipo = []
#         self.ls_tempo = []
#         self.ls_dict= [] 

#     def _get_taxa(self):
#         return 1 - 0.7/100
        
#     def _operacao_compra(self, por_para_ajustar, v_negociacao, tempo, busc_operacao):
#         btc_compra = (self.qnt_dinherio_atual * por_para_ajustar) / v_negociacao
#         self.btc_atual = self.btc_atual + (btc_compra * self._get_taxa())
#         self.qnt_dinherio_atual = self.qnt_dinherio_atual -  (self.qnt_dinherio_atual * por_para_ajustar)
#         self.ls_valor_carteira.append(self.qnt_dinherio_atual + self.btc_atual*v_negociacao )
#         self.ls_tipo.append("compra")
#         self.ls_tempo.append(tempo)

#         self.ls_dict.append({"tipo":"compra", 
#                             "busc_operacao": busc_operacao,
#                             "tempo":tempo, 
#                             "qnt_btc": btc_compra})
    
    

#     def _operacao_venda(self, por_para_ajustar, v_negociacao, tempo, busc_operacao):
#         btc_venda = self.btc_atual * por_para_ajustar
#         self.btc_atual = self.btc_atual - btc_venda

#         self.qnt_dinherio_atual = self.qnt_dinherio_atual + (btc_venda* v_negociacao * self._get_taxa())
#         self.ls_valor_carteira.append(self.qnt_dinherio_atual + self.btc_atual*v_negociacao )
#         self.ls_tipo.append("venda")
#         self.ls_tempo.append(tempo)

#         self.ls_dict.append({"tipo":"venda",
#                             "busc_operacao": busc_operacao,
#                             "tempo":tempo, 
#                             "qnt_btc": btc_venda})



#     def ajusta_portifolio_por(self, por_para_ajustar, v_negociacao, tempo, busc_operacao):
#         def get_porcento_atual():
#             s = self.btc_atual*v_negociacao * 100/(self.btc_atual*v_negociacao + self.qnt_dinherio_atual) # so nao pode ser zero

#             s =  s/100

#             return s 
        
#         r_oper_compra = por_para_ajustar >= get_porcento_atual()
#         r_oper_venda = por_para_ajustar < get_porcento_atual()
#         if r_oper_compra:
#             self._operacao_compra(por_para_ajustar - get_porcento_atual(), v_negociacao, tempo,busc_operacao)
#         if r_oper_venda:
#             self._operacao_venda(get_porcento_atual() - por_para_ajustar, v_negociacao, tempo, busc_operacao)



def constroi_ordem(negociado_compra, porcentagem, coin="XRP"):
    dic_ordem_criada = {"coin": coin,
                        "qnt": 0.2,
                        "compra": negociado_compra,
                        "venda": negociado_compra + porcentagem,
                        "fee_total": 0,
                        "lucro": 0,
                         "estado": "aberta"}
    
    return dic_ordem_criada

class Mercador_back_test_grid:
    def __init__(self, qnt_dinheiro, distancia):
        self.qnt_dinehiro_inicial = qnt_dinheiro 
        self.qnt_dinheiro_atual = qnt_dinheiro
        self.ls_qnt_dinheiro = []
        self.ordens = []
        self.distancia = distancia
    
    def _compra(self, ordem):
        self.qnt_dinheiro_atual = self.qnt_dinheiro_atual - (ordem["compra"] * ordem["qnt"])
        self.ordens.append(ordem)
        self.ls_qnt_dinheiro.append(self.qnt_dinheiro_atual)
        
    def cria_ordens(self, valor_compra):
        ordem = constroi_ordem(valor_compra, self.distancia)
        self._compra(ordem)
        
    def _termina_ordens(self,close, lis_ordens_a_serem_executadas):
        for ordem in lis_ordens_a_serem_executadas:
            ordem["estado"] = "fechada"
            ordem["lucro"] =  close - ordem["compra"]
            self.qnt_dinheiro_atual = self.qnt_dinheiro_atual + close

        self.ls_qnt_dinheiro.append(self.qnt_dinheiro_atual)    

                
    def executa_ordens(self, close):
    
        lis_ordens_aberta = list(filter(get_ordens_abertas, self.ordens))
        r_existe_ordens_abertas = len(lis_ordens_aberta) != 0
        if r_existe_ordens_abertas:
            
            lis_ordens_a_serem_executadas = list(filter(constroi_get(close),lis_ordens_aberta))
            r_exite_ordens_para_fexar = len(lis_ordens_a_serem_executadas) !=0
            if r_exite_ordens_para_fexar:
                self._termina_ordens(close,lis_ordens_a_serem_executadas)

def get_ordens_abertas(x):
    return x["estado"] == "aberta"
    
def constroi_get(close):
    def get_ordens_abertas_range(x):
        return x["venda"] < close
    return get_ordens_abertas_range


# btc = {"qnt_moeda": 1, "v_negociado":23423, "t_operaca": "buy!sell" }
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta
# import mplfinance as mpf
# from finta import TA
# def gerador_dados(df_criado):
#     for row in df_criado.iterrows():
#         yield row
