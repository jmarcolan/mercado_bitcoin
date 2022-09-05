import asyncio
import time
import datetime
import asyncio
import os


import estrategias as es
import get_dados as buscador
import trader as tr


clear = lambda: os.system('cls')


async def aciona_estrategia_aprimorada(bot_vivo, tempo=1):
    
    while True:
        try:
            # clear()
            print(20*f"-{bot_vivo.dados_bot['bot_id']}-X")
            buscador.atualiza_ultimo_criado(bot_vivo.dados_bot["coin"])
            v_limite_inf, v_limite_sup,v_close, r_valor_dentro_limite = es.faz_estrategia_live_aprimorada(
                        bot_vivo.dados_bot["limite_inferior"], 
                        bot_vivo.dados_bot["limite_superior"],
                        bot_vivo.dados_bot["grid_valor"], 
                        bot_vivo.dados_bot["coin"])

            print("-------------------------->")

            if r_valor_dentro_limite :

                bot_vivo.cria_ordens(v_limite_inf, v_close)
                bot_vivo.atualiza_ordens()
                print(f"Está dentro do limite {v_limite_inf} ao  {v_limite_sup} o valor {v_close}")

                print("-------------------------->")
                bot_vivo.print_ordens()
                
            else:
                print(f'O preço {v_close} Esta fora do limite máximo de {bot_vivo.dados_bot["limite_superior"]} ou minimo {bot_vivo.dados_bot["limite_inferior"]}')
                bot_vivo.print_ordens()

            print(f"O proximo em {datetime.datetime.now() + datetime.timedelta(minutes=tempo)}")
            print(20*f"-{bot_vivo.dados_bot['bot_id']}-X")
            await asyncio.sleep(tempo*60)

        except Exception as e: # work on python 3.x
            print("Na estrategia aconteceu alguma problema")
            print(e)
            # para nao ser block caso um dos bot exploda.
            await asyncio.sleep(tempo/2*60)
            # time.sleep(60)



#     break


async def async_main() -> None:
    try:
        # caso nao tenha nenhum bot no bd.
        tr.constroi_bd_bot()
        tr.constroi_bd_bot_operacao()
        
        bot_1 = tr.inicializa_bot(1, 20, 0.06, 1.9, 3.10, 0.5, "XRP")
        bd_m = tr.Bot_melhorado(bot_1)


        bot_2 = tr.inicializa_bot(2, 20, 0.04, 2.25, 2.7, 0.5,"XRP")
        bd_m_2 = tr.Bot_melhorado(bot_2)

        bot_3= tr.inicializa_bot(9, 40, 0.04, 2.7, 4.2, 1,"XRP")
        bd_m_3 = tr.Bot_melhorado(bot_3)

        # bot_3 = tr.inicializa_bot(4, 50, 0.04, 5, 5.8, 1.03, "USDC")
        # bd_m_3 = tr.Bot_melhorado(bot_3)



        await asyncio.gather( 
            
            aciona_estrategia_aprimorada(bd_m, 0.9),
            aciona_estrategia_aprimorada(bd_m_2, 0.9),
            aciona_estrategia_aprimorada(bd_m_3, 0.9)

            )

    except Exception as e:
        print(e)
        print("algum erro loco")

asyncio.run(async_main())



        # keep_printing("Pegando daods",1)
        # keep_printing("Pegando daods",1),
        # keep_printing("Ativando robo",5)

# async def keep_printing(name :str ="", tempo=1)-> None:
#     while True:
#         print(f"{name} esta sendo ativo a cada {tempo} segundo")
#         print(datetime.datetime.now())
#         print(f"proximo em {datetime.datetime.now() + datetime.timedelta(minutes=1)}")
#         try:
#             await asyncio.sleep(tempo)
#         except:
#             print("por algum motivo parou de funcionar")
#             break



# async def aciona_estrategia(bot_vivo, tempo=5):
    
#     while True:
#         try:
#             clear()
#             print(10*"-X-X-X")
#             r_aciona,v_close = es.faz_estrategia_live(0.06,"XRP")
#             if r_aciona:
#                 bot_vivo.cria_ordens(v_close)
#                 print(f"o bot foi acionado {v_close}")
#             else:
#                 print("bot não acionado")

#             bot_vivo.print_ordens()
#             print(f"O proximo em {datetime.datetime.now() + datetime.timedelta(minutes=tempo)}")
#             print(10*"-X-X-X")

#             await asyncio.sleep(tempo*60)

#         except Exception as e: # work on python 3.x
#             print("A parte de fazer estretagia foi desligada")
#             print(e)
#             break


# async def atualiza_dados(bot_vivo, tempo=1.2, moeda="XRP"):
#     while True:
#         try:
#             clear()
#             print(10*"-[]-[]-[]")
#             buscador.atualiza_ultimo_criado(moeda)
#             bot_vivo.atualiza_ordens()
            
#             # print(f"O buscador de dados esta sendo ativo a cada {tempo} minutos")
#             bot_vivo.print_ordens()
#             print(f"O proximo em {datetime.datetime.now() + datetime.timedelta(minutes=tempo)}") 
#             print(10*"-[]-[]-[]")
#             await asyncio.sleep(tempo*60)
#         except Exception as e:
#             print(e)
#             print("O buscador de dados foi desligado")
#             break
