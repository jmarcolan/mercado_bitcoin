import asyncio
import time
import datetime
import asyncio


import estrategias as es
import get_dados as buscador
import trader as tr

async def aciona_estrategia(bot_vivo, tempo=5):
    
    while True:
        try:
            r_aciona,v_close = es.faz_estrategia_live(0.06,"XRP")
            if r_aciona:
                bot_vivo.cria_ordens(v_close)

            else:
                print("bot não acionado")

            print(10*"-X-X-X")
            print(f"O valor {v_close} acionou ? {r_aciona}")
            print(f"O acionador de dados esta sendo ativo a cada {tempo} minutos")
            print(f"O proximo em {datetime.datetime.now() + datetime.timedelta(minutes=tempo)}")
            print(10*"-X-X-X")

            await asyncio.sleep(tempo*60)

        except:
            print("A parte de fazer estretagia foi desligada")
            break


async def atualiza_dados(bot_vivo, tempo=0.8, moeda="XRP"):
    while True:
        try:
            print(10*"-[]-[]-[]")
            buscador.atualiza_ultimo_criado(moeda)
            bot_vivo.atualiza_ordens()
            
            print(f"O buscador de dados esta sendo ativo a cada {tempo} minutos")
            print(f"O proximo em {datetime.datetime.now() + datetime.timedelta(minutes=tempo)}") 
            print(10*"-[]-[]-[]")
            await asyncio.sleep(tempo*60)
        except:
            print("O buscador de dados foi desligado")
            break




async def async_main() -> None:
    try:
        bot = tr.inicializa_bot(4,20)
        bd = tr.Boot_dados(bot, 0.11)


        await asyncio.gather( 
            atualiza_dados(bd),
            aciona_estrategia(bd)
           )

    except:
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