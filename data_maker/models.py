#### python
# filepath: c:\Users\ns69a\allpokemon0301\backend\data_maker\models.py
from tkinter import N
from django.db import models

class S1_Endpoint(models.Model):
    ep_id = models.IntegerField(primary_key=True, default=0)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    total_ids = models.IntegerField(blank=True, null=True)
    exist_ids = models.JSONField(default=list)

    def __str__(self):
        return self.name

class BaseRawData(models.Model):
    id_str = models.CharField(max_length=100, unique=True, primary_key=True)
    id_int = models.IntegerField(unique=True)
    name_in_data = models.CharField(max_length=100)
    ep_url = models.CharField(max_length=200)
    raw_data = models.JSONField()
    json_exist = models.BooleanField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Set json_exist to True if raw_data is not empty
        self.json_exist = bool(self.raw_data)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_in_data

    class Meta:
        abstract = True

class S2_PokemonSpeciesRawData(BaseRawData):
    class Meta:
        __module__ = __name__

class S2_PokemonRawData(BaseRawData):
    class Meta:
        __module__ = __name__

class S2_PokemonFormRawData(BaseRawData):
    class Meta:
        __module__ = __name__

class S2_AbilityRawData(BaseRawData):
    class Meta:
        __module__ = __name__

class S2_ItemRawData(BaseRawData):
    class Meta:
        __module__ = __name__

class S2_MoveRawData(BaseRawData):
    class Meta:
        __module__ = __name__
        
class S3_MonsterIndividual(models.Model):
    monster_id_int = models.IntegerField(primary_key=True)
    monster_id_str = models.CharField(max_length=100,)
    pokemon = models.ForeignKey(S2_PokemonRawData, on_delete=models.CASCADE)
    pokemon_short_json = models.JSONField(blank=True, null=True)
    pokemon_species = models.ForeignKey(S2_PokemonSpeciesRawData, on_delete=models.CASCADE)
    pokemon_species_short_json = models.JSONField(blank=True, null=True)
    pokemon_form = models.ForeignKey(S2_PokemonFormRawData, on_delete=models.CASCADE)
    pokemon_form_short_json = models.JSONField(blank=True, null=True)
    exist_all_json = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.monster_id_str
    
    
class S5_DemoMonseterIndividual(models.Model):
    monster_id_int = models.IntegerField(primary_key=True)
    monster_id_str = models.CharField(max_length=100,)
    
class S6_ProcessedPokemon(models.Model):
    """
    S3_MonsterIndividual が持つ3つのJSONを統合・整形し、
    最終的に必要な形で保持するモデル。
    ここでは例として主な項目をフィールド化している。
    """
    monster_id_int = models.IntegerField(primary_key=True)
    monster_id_str = models.CharField(max_length=100, blank=True, null=True)
    national_number = models.IntegerField(blank=True, null=True)
    monster_name = models.CharField(max_length=100, blank=True, null=True)
    monster_name_jp = models.CharField(max_length=100, blank=True, null=True)
    form_name = models.CharField(max_length=100, blank=True, null=True)
    form_name_jp = models.CharField(max_length=100, blank=True, null=True)
    type_1 = models.CharField(max_length=100, blank=True, null=True)
    type_2 = models.CharField(max_length=100, blank=True, null=True)
    ability_1 = models.CharField(max_length=100, blank=True, null=True)
    ability_2 = models.CharField(max_length=100, blank=True, null=True)
    ability_3 = models.CharField(max_length=100, blank=True, null=True)
    flavor_text = models.CharField(max_length=300, blank=True, null=True)
    egg_groups = models.JSONField(blank=True, null=True)
    stat_h = models.IntegerField(blank=True, null=True)
    stat_a = models.IntegerField(blank=True, null=True)
    stat_b = models.IntegerField(blank=True, null=True)
    stat_c = models.IntegerField(blank=True, null=True)
    stat_d = models.IntegerField(blank=True, null=True)
    stat_s = models.IntegerField(blank=True, null=True)
    stat_t = models.IntegerField(blank=True, null=True)
    pokedex_number = models.JSONField(blank=True, null=True)
    is_genera = models.CharField(max_length=100, blank=True, null=True)
    is_mega = models.BooleanField(default=False)
    is_gmax = models.BooleanField(default=False)
    is_normal = models.BooleanField(default=False)
    is_baby = models.BooleanField(default=False)
    is_legendary = models.BooleanField(default=False)
    is_mythical = models.BooleanField(default=False)
    front_url = models.CharField(max_length=200, blank=True, null=True)
    front_url_exist = models.BooleanField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.monster_name} ({self.monster_id_int})"
    
    