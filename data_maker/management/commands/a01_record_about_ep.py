from django.core.management.base import BaseCommand
from data_maker.models import S1_Endpoint

class Command(BaseCommand):
    help = "Record endpoints to the database"

    def handle(self, *args, **kwargs):
        pokemon_species_ep = {"name": "pokemon-species", "url": "https://pokeapi.co/api/v2/pokemon-species/"}
        pokemon_ep = {"name": "pokemon", "url": "https://pokeapi.co/api/v2/pokemon/"}
        pokemon_form_ep = {"name": "pokemon-form", "url": "https://pokeapi.co/api/v2/pokemon-form/"}
        ability_ep = {"name": "ability", "url": "https://pokeapi.co/api/v2/ability/"}
        move_ep = {"name": "move", "url": "https://pokeapi.co/api/v2/move/"}
        item_ep = {"name": "item", "url": "https://pokeapi.co/api/v2/item/"}
        
        endpoints = [pokemon_species_ep, pokemon_ep, pokemon_form_ep, ability_ep, move_ep, item_ep]
        for idx, endpoint in enumerate(endpoints):
            S1_Endpoint.objects.create(ep_id=idx, **endpoint)
