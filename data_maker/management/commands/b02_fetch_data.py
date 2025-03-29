import asyncio
import aiohttp
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from data_maker.models import S1_Endpoint
from data_maker.models import (
    S2_PokemonSpeciesRawData,
    S2_PokemonRawData,
    S2_PokemonFormRawData,
    S2_AbilityRawData,
    S2_ItemRawData,
    S2_MoveRawData,
)

class Command(BaseCommand):
    help = "Fetch data from the endpoints and store them in the database"

    def handle(self, *args, **kwargs):
        self.clear()
        asyncio.run(self.register())

    def clear(self, *args, **kwargs):
        S2_PokemonSpeciesRawData.objects.all().delete()
        S2_PokemonRawData.objects.all().delete()
        S2_PokemonFormRawData.objects.all().delete()
        S2_AbilityRawData.objects.all().delete()
        S2_ItemRawData.objects.all().delete()
        S2_MoveRawData.objects.all().delete()

    async def register(self, *args, **kwargs):
        endpoints = await sync_to_async(list)(S1_Endpoint.objects.iterator())
        async with aiohttp.ClientSession() as session:
            for endpoint in endpoints:
                base_url = endpoint.url
                ids = endpoint.exist_ids
                async with asyncio.TaskGroup() as tg:
                    tasks = {}
                    for id_ in ids:
                        url = f"{base_url}{id_}/"
                        tasks[id_] = tg.create_task(self.get_single_data(session, url))
                        
                for id_, task in tasks.items():
                    try:
                        data = task.result()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error fetching id {id_}: {e}"))
                        continue

                    endpoint_name = endpoint.name
                    results = {
                        "id_str": str(id_).zfill(5),
                        "id_int": id_,
                        "name_in_data": data["name"],
                        "ep_url": f"{base_url}{id_}/",
                        "raw_data": data,
                    }
                    if endpoint_name == "pokemon-species":
                        await sync_to_async(S2_PokemonSpeciesRawData.objects.create)(**results)
                    elif endpoint_name == "pokemon":
                        await sync_to_async(S2_PokemonRawData.objects.create)(**results)
                    elif endpoint_name == "pokemon-form":
                        await sync_to_async(S2_PokemonFormRawData.objects.create)(**results)
                    elif endpoint_name == "ability":
                        await sync_to_async(S2_AbilityRawData.objects.create)(**results)
                    elif endpoint_name == "item":
                        await sync_to_async(S2_ItemRawData.objects.create)(**results)
                    elif endpoint_name == "move":
                        await sync_to_async(S2_MoveRawData.objects.create)(**results)
                    else:
                        self.stdout.write("Unknown endpoint name")

    async def get_single_data(self, session, url):
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return data
