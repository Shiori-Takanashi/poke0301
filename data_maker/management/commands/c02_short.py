import re
import types
from django.core.management.base import BaseCommand
import json

from data_maker.models import (
    S3_MonsterIndividual
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.clear()
        monster_indviduals = S3_MonsterIndividual.objects.iterator()
        for monster_indvidual in monster_indviduals:
            pokemon_raw_data = monster_indvidual.pokemon
            pokemon_species_raw_data = monster_indvidual.pokemon_species
            pokemon_form_raw_data = monster_indvidual.pokemon_form
            pokemon_short_data = self.short_json(pokemon_raw_data.raw_data)
            pokemon_species_short_data = self.short_json(pokemon_species_raw_data.raw_data)
            pokemon_form_short_data = self.short_json(pokemon_form_raw_data.raw_data)
            monster_indvidual.pokemon_short_json = pokemon_short_data
            monster_indvidual.pokemon_species_short_json = pokemon_species_short_data
            monster_indvidual.pokemon_form_short_json = pokemon_form_short_data
            monster_indvidual.save()

    def clear(self):
        S3_MonsterIndividual.objects.all().update(
            pokemon_short_json=None,
            pokemon_species_short_json=None,
            pokemon_form_short_json=None
        )
        
    def short_json(self, raw_data):
        short_data = {
            "jp_name": self.jp_name(raw_data),
            "types": self.types(raw_data),
            "abilities": self.abilities(raw_data),
            "cries": self.cries(raw_data),
            "stats": self.stats(raw_data),
            "sprites": self.sprites(raw_data),
            "past_types": self.past_types(raw_data),
            "form_name": self.form_name(raw_data),
            "form_name_from_names": self.form_names(raw_data),
            "name": self.name(raw_data),
            "flavor_text": self.flavor_text(raw_data),
            "egg_group": self.egg_group(raw_data),
            "form_description": self.form_description(raw_data),
            "first_generation": self.first_generation(raw_data),
            "genera": self.what_genera(raw_data),
            'is_mega': self.is_mega(raw_data),
            'is_gmax': self.is_gmax(raw_data),
            "is_baby": self.is_baby(raw_data),
            "is_legendary": self.is_legendary(raw_data),
            "is_mythical": self.is_mythical(raw_data),
            "pokedex_number": self.pokedex_number(raw_data),
        }
        return short_data

            
    def jp_name(self, data):
        names = data.get('names', [])
        if names:
            jp_name = [entry["name"] for entry in names if entry["language"]["name"] == "ja-Hrkt"]
            if jp_name:
                return jp_name[0]
            else:
                return "No jp name"
        else:
            return "No names key"
        
    def types(self, data):
        types = data.get('types', [])
        all_types = []
        for type_ in types:
            all_types.append(type_["type"]["name"])
        if all_types:
            return all_types
        else:
            return "No types key"
            
    def abilities(self, data):
        abilities = data.get('abilities', [])
        all_abilities = []
        for ability in abilities:
            all_abilities.append(ability["ability"]["name"])
            
        length = len(all_abilities)
        if length == 0:
            return "No abilities key"
        elif length == 1:
            return all_abilities[0]
        elif length == 2:
            if all_abilities[0] == all_abilities[1]:
                return all_abilities[0]
            else:
                return all_abilities
        elif length == 3:
            if all_abilities[0] == all_abilities[1] == all_abilities[2]:
                return all_abilities[0]
            elif all_abilities[0] == all_abilities[1]:
                return [all_abilities[0], all_abilities[2]]
            elif all_abilities[1] == all_abilities[2]:
                return [all_abilities[0], all_abilities[1]]
            else:
                return all_abilities
            
    def cries(self, data):
        cries = data.get('cries', [])
        if not cries:
            return "No cries key"
        elif cries["latest"]:
            return cries["latest"]
        elif cries["legacy"]:
            return cries["legacy"]
        else:
            return "cries key have nothing"
        
        
    def stats(self, data):
        stats = data.get('stats', [])
        all_stats = []
        if stats:
            for stat in stats:
                all_stats.append(stat["base_stat"])
            if all_stats:
                return all_stats
            else:
                return "stats key have nothing"
        else:
            return "No stats key"
        
    def sprites(self, data):
        sprites_data = data.get('sprites')
        if not sprites_data:
            return "No sprites key"
        
        all_sprites = []

        # 第1階層
        for k1, v1 in sprites_data.items():
            if isinstance(v1, str):
                all_sprites.append((k1, v1))
            elif isinstance(v1, dict):
                # 第2階層
                for k2, v2 in v1.items():
                    if isinstance(v2, str):
                        all_sprites.append((f"{k1} - {k2}", v2))
                    elif isinstance(v2, dict):
                        # 第3階層
                        for k3, v3 in v2.items():
                            if isinstance(v3, str):
                                all_sprites.append((f"{k1} - {k2} - {k3}", v3))
                            elif isinstance(v3, dict):
                                # 第4階層
                                for k4, v4 in v3.items():
                                    if isinstance(v4, str):
                                        all_sprites.append((f"{k1} - {k2} - {k3} - {k4}", v4))
                                    elif isinstance(v4, dict):
                                        # 第5階層
                                        for k5, v5 in v4.items():
                                            if isinstance(v5, str):
                                                all_sprites.append((f"{k1} - {k2} - {k3} - {k4} - {k5}", v5))
                                            elif isinstance(v5, dict):
                                                # 5階層を超えた辞書
                                                print("too deep!")
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

        return all_sprites

    
    def past_types(self, data):
        past_types = data.get('past_types', [])
        if past_types:
            return past_types
        else:
            return "No past_types"
        
    def form_name(self, data):
        form_name = data.get('form_name', "")
        if form_name:
            return form_name
        else:
            return "No form_name"
        
    def form_names(self, data):
        form_names = data.get('form_names', [])
        if not form_names:
            return "No form_names"
        
        # 優先度順に探すリストを作成
        priority = ["ja-Hrkt", "ja", "en"]
        
        for lang in priority:
            for form_name in form_names:
                if form_name["language"]["name"] == lang:
                    return form_name["name"]
        
        return "No form_names"
            
    def name(self, data):
        name = data.get('name', "")
        if name:
            return name
        else:
            return "No name"
        
    def flavor_text(self, data):
        flavor_text_entries = data.get('flavor_text_entries', [])
        if not flavor_text_entries:
            return "No flavor_text_entries"
        
        # 優先度順に探すリストを作成
        priority = ["ja-Hrkt", "ja", "en"]
        
        for lang in priority:
            for flavor_text_entry in flavor_text_entries:
                if flavor_text_entry["language"]["name"] == lang:
                    return flavor_text_entry["flavor_text"]
        
        return "No flavor_text_entries"
    
    def egg_group(self,data):
        egg_groups = data.get('egg_groups', [])
        if egg_groups:
            egg_groups_list = []
            for egg_group in egg_groups:
                egg_groups_list.append(egg_group["name"])
            return egg_groups_list
        else:
            return "No egg_groups"
        
    def form_description(self, data):
        form_descriptions = data.get('form_descriptions', [])
        if form_descriptions:
            return form_descriptions
        else:
            return "No form_descriptions"
        
    def first_generation(self, data):
        first_generation = data.get('generation', "")
        if first_generation:
            return first_generation["name"]
        else:
            return "No first_generation"
        
    def what_genera(self, data):
        genera = data.get('genera', [])
        if not genera:
            return "No genera key"
        priority = ["ja-Hrkt", "ja", "en"]
        
        for lang in priority:
            for gen in genera:
                if gen["language"]["name"] == lang:
                    return gen["genus"]
                
    def is_mega(self, data):
        form_type = data.get('form_type', "")
        if form_type == "mega":
            return True
        else:
            return False
        
    def is_gmax(self, data):
        form_type = data.get('form_type', "")
        if form_type == "gmax":
            return True
        else:
            return False
        
    def is_baby(self, data):
        is_baby = data.get('is_baby', False)
        if is_baby:
            return True
        else:
            return False
        
    def is_legendary(self, data):
        is_legendary = data.get('is_legendary', False)
        if is_legendary:
            return True
        else:
            return False
        
    def is_mythical(self, data):
        is_mythical = data.get('is_mythical', False)
        if is_mythical:
            return True
        else:
            return False
        
    def pokedex_number(self, data):
        pokedex_numbers = data.get('pokedex_numbers', [])
        results = []
        if pokedex_numbers:
            for pokedex_number in pokedex_numbers:
                number = pokedex_number["entry_number"]
                name = pokedex_number["pokedex"]["name"]
                results.append({name: number})
        else:
            return "No pokedex_numbers"
        return results
    
    def no_meaning_key_del(self, data):
        result = {}
        
        # Extract the is_* values
        is_baby = data.get("is_baby", False)
        is_legendary = data.get("is_legendary", False)
        is_mythical = data.get("is_mythical", False)
        
        # Check if all three are False
        all_false = not (is_baby or is_legendary or is_mythical)
        
        for key, value in data.items():
            # Skip keys where value is "No something" or "something have nothing"
            if isinstance(value, str) and (value.startswith("No ") or "have nothing" in value):
                continue
            
            # For is_* keys, only add them if they are True
            if key in ["is_baby", "is_legendary", "is_mythical"]:
                if value:
                    result[key] = value
            else:
                result[key] = value
        
        # Add is_normal = True if all three is_* are False
        if all_false:
            result["is_normal"] = True
                
                
        return result