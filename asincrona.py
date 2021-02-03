import asyncio
import time
import datetime
import asyncio

import get_dados as buscador

async def pega_dados(tempo,moeda="XRP"):
    while True:
        buscador.atualiza_ultimo_criado(moeda)
        print(f"O buscador de dados esta sendo ativo a cada {tempo} minutos proximo em {datetime.datetime.now() + datetime.timedelta(minutes=1)}")
        try:
            await asyncio.sleep(tempo*60)
        except:
            print("foi desligado")
            break


async def keep_printing(name :str ="", tempo=1)-> None:
    while True:
        print(f"{name} esta sendo ativo a cada {tempo} segundo")
        print(datetime.datetime.now())
        print(f"proximo em {datetime.datetime.now() + datetime.timedelta(minutes=1)}")
        try:
            await asyncio.sleep(tempo)
        except:
            print("por algum motivo parou de funcionar")
            break

async def async_main() -> None:
    try:
        # asyncio.wait_for
        await asyncio.gather( 
        #    pega_dados(1,"XRP")
           keep_printing("Pegando daods",1)
           )
        # keep_printing("Pegando daods",1),
        # keep_printing("Ativando robo",5)
    except:
        print("algum erro loco")


asyncio.run(async_main())