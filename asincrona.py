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
            clear()
            print(10*"-X-X-X")
            buscador.atualiza_ultimo_criado("XRP")
            v_limite_inf, v_limite_sup, v_close = es.faz_estrategia_live_aprimorada(1.9, 3.10, 0.06,"XRP")

            print("-------------------------->")
            bot_vivo.cria_ordens(v_limite_inf, v_close)
            bot_vivo.atualiza_ordens()
            print(f"Está dentro do limite {v_limite_inf} ao  {v_limite_sup} o valor{v_close}")

            print("-------------------------->")
            bot_vivo.print_ordens()
            print(f"O proximo em {datetime.datetime.now() + datetime.timedelta(minutes=tempo)}")
            print(10*"-X-X-X")

            await asyncio.sleep(tempo*60)

        except Exception as e: # work on python 3.x
            print("Na estrategia aconteceu alguma cois")
            print(e)
        #     break



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




async def async_main() -> None:
    try:
        bot = tr.inicializa_bot(7)
        bd = tr.Bot_melhorado(bot, 0.13)


        await asyncio.gather( 
            # atualiza_dados(bd),
            aciona_estrategia_aprimorada(bd, 0.8)
            # aciona_estrategia(bd)
            )

    except Exception as e:
        print(e)
        print("algum erro loco")


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


asyncio.run(async_main())