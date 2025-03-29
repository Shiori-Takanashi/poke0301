from rest_framework import serializers
from data_maker.models import S6_ProcessedPokemon

class ProcessedPokemonNameJpSerializer(serializers.ModelSerializer):
    class Meta:
        model = S6_ProcessedPokemon
        fields = (
                    'monster_id_str',
                    'monster_name_jp',
                    'type_1', 'type_2',
                    'ability_1', 'ability_2', 'ability_3',
                    'stat_h', 'stat_a', 'stat_b', 'stat_c', 'stat_d', 'stat_s', 'stat_t',
                    'front_url'
                )
