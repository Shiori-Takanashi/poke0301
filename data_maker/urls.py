from django.urls import path
from data_maker.views import RandomPokemonNameJpView

urlpatterns = [
    path('api/random/', RandomPokemonNameJpView.as_view(), name='random_pokemon_name_jp'),
]
