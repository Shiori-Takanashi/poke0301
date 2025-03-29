from django.core.management.base import BaseCommand
from data_maker.models import S3_MonsterIndividual
from data_maker.models import S2_PokemonRawData, S2_PokemonSpeciesRawData, S2_PokemonFormRawData

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.clear()
        self.register()
        
    def clear(self):
        S3_MonsterIndividual.objects.all().delete()
        
    def register(self):
        all_pokemon_species = S2_PokemonSpeciesRawData.objects.iterator()
        monster_id_int = 1
        for pokemon_species in all_pokemon_species:
            result = {}
            # pokemon-speciesを登録
            result.update({'pokemon_species': pokemon_species})
            pokemon_varieties = pokemon_species.raw_data['varieties']
            for pokemon_variety in pokemon_varieties:
                pokemon_url = pokemon_variety["pokemon"]["url"]
                pokemon_id_str = pokemon_url.split("/")[-2].zfill(5)
                pokemon = S2_PokemonRawData.objects.get(id_str=pokemon_id_str)
                # pokemonを登録
                result.update({"pokemon": pokemon})
                
                pokemon_forms = pokemon.raw_data.get("forms", [])
                for pokemon_form in pokemon_forms:
                    pokemon_form_url = pokemon_form["url"]
                    pokemon_form_id_str = pokemon_form_url.split("/")[-2].zfill(5)
                    # pokemon-formを登録
                    pokemon_form = S2_PokemonFormRawData.objects.get(id_str=pokemon_form_id_str)
                    result.update({"pokemon_form": pokemon_form})
                    result.update({"monster_id_int": monster_id_int})
                    monster_id_str = str(monster_id_int).zfill(5)
                    result.update({"monster_id_str": monster_id_str})
                    pokemon_individual = S3_MonsterIndividual(**result)
                    pokemon_individual.save()
                    monster_id_int += 1
                    
                
            
            
            
            
            
            
            