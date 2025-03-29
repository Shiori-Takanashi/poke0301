# ファイル: data_maker/management/commands/import_processed_pokemon.py
from django.core.management.base import BaseCommand
from data_maker.models import (
    S2_AbilityRawData,
    S3_MonsterIndividual,
    S6_ProcessedPokemon
)
from tqdm import tqdm




class Command(BaseCommand):
    help = "S3_MonsterIndividual の3つのJSONを整理して S6_ProcessedPokemon に登録・更新するコマンド"

    def handle(self, *args, **options):
        monsters = S3_MonsterIndividual.objects.iterator()
        old_S6 = S6_ProcessedPokemon.objects.all()
        old_S6.delete()
        monster_id_int = 1
        for monster in tqdm(monsters):
            # まずフィールドを初期化
            pokemon_json = monster.pokemon_short_json or {}
            species_json = monster.pokemon_species_short_json or {}
            form_json = monster.pokemon_form_short_json or {}
            
            pokedex_national_number = species_json.get("pokedex_number",[])[0].get("national","")
            monster_id_str = self.get_monster_id_str(pokedex_national_number)

            sprites = form_json.get("sprites")  # sprites が存在すればリストを取得
            front_url = None
            if sprites:
                for sprite in sprites:
                    # 各 sprite は ["キー", "URL"] の形式を想定
                    if sprite[0] == "front_default":
                        front_url = sprite[1]
                        break

            
            # ▼ name / jp_name
            # pokemon_short_json の "name"
            name = pokemon_json.get("name") or ""
            # species の jp_name
            name_jp = species_json.get("jp_name") or ""
            
            # ▼ form name
            form_name = form_json.get("form_name") or ""
            form_name_jp = form_json.get("form_name_from_names") or ""

            # ▼ types
            # pokemon_short_json / form_json いずれにあるか確認して使う
            # Gigantamax(フォルム)だと form_json に types が入る場合もあるため
            types = None
            if pokemon_json.get("types") and isinstance(pokemon_json["types"], list):
                types = pokemon_json["types"]
                length = len(types)
                if length == 1:
                    type_1 = self.translate_type(types[0])
                    type_2 = None
                elif length == 2:
                    type_1 = self.translate_type(types[0])
                    type_2 = self.translate_type(types[1])
                    
            
            # ▼ abilities
            ability_1_jp = ability_2_jp = ability_3_jp = None
            abilities = pokemon_json.get("abilities")
            if type(abilities) is str:
                ability_1_jp = self.translate_ability(abilities)
                ability_2_jp = ability_3_jp = None
            elif not abilities:
                ability_1_jp = ability_2_jp = ability_3_jp = None
            elif len(abilities) == 1:
                ability_1_jp = self.translate_ability(abilities[0])
                ability_2_jp = ability_3_jp = None
            elif len(abilities) == 2:
                ability_1_jp = self.translate_ability(abilities[0])
                ability_2_jp = self.translate_ability(abilities[1])
                ability_3_jp = None
            elif len(abilities) == 3:
                ability_1_jp = self.translate_ability(abilities[0])
                ability_2_jp = self.translate_ability(abilities[1])
                ability_3_jp = self.translate_ability(abilities[2])
            else:
                # デバッグ用ログを追加
                print("Debug:", monster_id_str, "abilities =", abilities)
                print(monster_id_str, len(abilities))
                
                

            # ▼ stats
            stats = pokemon_json.get("stats") if pokemon_json.get("stats") else None
            if stats:
                stat_h = stats[0]
                stat_a = stats[1]
                stat_b = stats[2]
                stat_c = stats[3]
                stat_d = stats[4]
                stat_s = stats[5]
                stat_t = sum(stats[0:6])
            else:
                stat_h = stat_a = stat_b = stat_c = stat_d = stat_s = stat_t = None

            # ▼ flavor_text
            # 通常は species_json から取得。フォーム固有の説明がある場合は form_json に入っている場合もある。
            flavor_text = None
            if species_json.get("flavor_text") and species_json["flavor_text"] != "no flavor_text_entries":
                flavor_text = species_json["flavor_text"]
            elif pokemon_json.get("flavor_text") and pokemon_json["flavor_text"] != "no flavor_text_entries":
                flavor_text = pokemon_json["flavor_text"]
            elif form_json.get("flavor_text") and form_json["flavor_text"] != "no flavor_text_entries":
                flavor_text = form_json["flavor_text"]

            # ▼ egg_groups
            # species_json に egg_group があるか確認
            egg_groups = species_json.get("egg_group") if species_json.get("egg_group") else None

            # ▼ pokedex_number
            # species_json の pokedex_number はリスト。なければ "no pokedex_numbers" の場合もある
            pokedex_number = None
            if isinstance(species_json.get("pokedex_number"), list):
                pokedex_number = species_json["pokedex_number"]

            # ▼ is_baby / is_legendary / is_mythical
            what_genera = species_json.get("genera", [])
            is_baby = species_json.get("is_baby", pokemon_json.get("is_baby", False))
            is_legendary = species_json.get("is_legendary", pokemon_json.get("is_legendary", False))
            is_mythical = species_json.get("is_mythical", pokemon_json.get("is_mythical", False))
            is_normal = not (is_baby or is_legendary or is_mythical)

            
            if form_name_jp.startswith("メガ"):
                # メガフォルムの場合は、form_name_jp をそのまま採用
                name_jp = form_name_jp
            elif form_name_jp.startswith("Gigantamax"):
                # Gigantmax の場合は、もとの name_jp に「（キョダイマックス）」を付与
                name_jp = name_jp + "（キョダイマックス）"
            elif form_name_jp.endswith("すがた"):
                # 「すがた」で終わる場合は、付与
                name_jp = name_jp + f"（{form_name_jp}）"
            elif form_name_jp != "No form_names" and self.is_all_halfwidth(form_name_jp):
                # 半角文字だけの場合は、付与
                name_jp = name_jp + f"（{form_name_jp}）"
            elif form_name != "No form_name":
                name_jp = name_jp + f"（{form_name}）"
                        


            
            # ▼ S6_ProcessedPokemon にアップサート(update or create)
            obj, created = S6_ProcessedPokemon.objects.update_or_create(
                monster_id_int=monster_id_int,
                defaults={
                    'monster_id_str': monster_id_str,
                    'monster_name': name,
                    'national_number': pokedex_national_number,
                    'monster_name_jp': name_jp,
                    'form_name': form_name,
                    'form_name_jp': form_name_jp,
                    'type_1': type_1,
                    'type_2': type_2,
                    'ability_1': ability_1_jp,
                    'ability_2': ability_2_jp,
                    'ability_3': ability_3_jp,
                    'stat_h': stat_h,
                    'stat_a': stat_a,
                    'stat_b': stat_b,
                    'stat_c': stat_c,
                    'stat_d': stat_d,
                    'stat_s': stat_s,
                    'stat_t': stat_t,
                    # 'stats': stats,  ← この行を削除
                    'flavor_text': flavor_text,
                    'egg_groups': egg_groups,
                    'pokedex_number': pokedex_number,
                    'is_genera': what_genera,
                    "is_normal": is_normal,
                    'is_baby': is_baby,
                    'is_legendary': is_legendary,
                    'is_mythical': is_mythical,
                    "front_url": front_url,
                    'front_url_exist': bool(front_url)
                }
            )
            monster_id_int += 1
            

            # ログ出力（任意）
        print("S6_ProcessedPokemon への登録が完了しました。")

    def is_all_halfwidth(self, s: str) -> bool:
        """
        入力文字列が全て半角文字（ASCII のスペース(0x20)～チルダ(0x7E)）で構成されているかを判定します。
        全て半角の場合は True、そうでない場合は False を返します。
        """
        if s == "No form_names":
            return False
        else:
            return s

    def translate_ability(self, ability_en: str) -> str:
        if not ability_en:
            return None
        ability_obj = S2_AbilityRawData.objects.filter(name_in_data=ability_en).first()
        if not ability_obj:
            return None
        ability_raw_data = ability_obj.raw_data
        ability_names = ability_raw_data.get("names")
        for ability_name in ability_names:
            if ability_name["language"]["name"] == "ja-Hrkt":
                return ability_name["name"]
            
    def translate_type(self, type_en: str) -> str:
        pokemon_types = {
            "normal": "普",    # ノーマル
            "fire": "炎",      # ほのお
            "water": "水",     # みず
            "electric": "電",  # でんき
            "grass": "草",     # くさ
            "ice": "氷",       # こおり
            "fighting": "闘",  # かくとう
            "poison": "毒",    # どく
            "ground": "地",    # じめん
            "flying": "飛",    # ひこう
            "psychic": "念",   # エスパー
            "bug": "虫",       # むし
            "rock": "岩",      # いわ
            "ghost": "幽",     # ゴースト
            "dragon": "竜",    # ドラゴン
            "dark": "悪",      # あく
            "steel": "鋼",     # はがね
            "fairy": "妖"      # フェアリー
        }
        return pokemon_types.get(type_en, "???")
    
    def get_monster_id_str(self, pokedex_national_number: str) -> str:
        monster_id_str_prefix = str(pokedex_national_number).zfill(4)
        num_of_same_id_str = S6_ProcessedPokemon.objects.filter(monster_id_str__startswith=monster_id_str_prefix).count()
        monster_id_str_suffix = str(num_of_same_id_str).zfill(2)
        return f"{monster_id_str_prefix}-{monster_id_str_suffix}"
