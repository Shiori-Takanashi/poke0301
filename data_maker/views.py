from rest_framework.views import APIView
from rest_framework.response import Response
from data_maker.models import S6_ProcessedPokemon
from data_maker.serializers import ProcessedPokemonNameJpSerializer

class RandomPokemonNameJpView(APIView):
    """
    リクエストごとにランダムで1匹の日本語のポケモン名（monster_name_jp）を返すビュー
    """
    def get(self, request, *args, **kwargs):
        random_pokemon = S6_ProcessedPokemon.objects.filter(
            front_url_exist=True,
            ability_1__isnull=False,
            ability_2__isnull=False,
            ability_3__isnull=False,
        ).exclude(
            monster_name_jp__icontains="totem"
        ).order_by('?').first()
        serializer = ProcessedPokemonNameJpSerializer(random_pokemon)
        return Response(serializer.data)

