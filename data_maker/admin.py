from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    S1_Endpoint,
    S2_PokemonSpeciesRawData,
    S2_PokemonRawData,
    S2_PokemonFormRawData,
    S2_AbilityRawData,
    S2_ItemRawData,
    S2_MoveRawData,
    S3_MonsterIndividual,
    S6_ProcessedPokemon
)


@admin.register(S1_Endpoint)
class S1_EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    ordering = ('ep_id',)


class BaseRawDataAdmin(admin.ModelAdmin):
    list_display = ('id_str', 'id_int', 'name_in_data', 'ep_url', 'json_exist',)
    ordering = ('id_str',)
    formfield_overrides = {
    JSONField: {
        'widget': JSONEditorWidget(
            options={'mode': 'form'},
            attrs={'style': 'width: 85%; height: 600px;'}
        )
    },
}


# 複数の RawData モデルをまとめて登録
raw_data_models = [
    S2_PokemonSpeciesRawData,
    S2_PokemonRawData,
    S2_PokemonFormRawData,
    S2_AbilityRawData,
    S2_ItemRawData,
    S2_MoveRawData
]
for model in raw_data_models:
    admin.site.register(model, BaseRawDataAdmin)


@admin.register(S3_MonsterIndividual)
class S3_MonsterIndividualAdmin(admin.ModelAdmin):
    list_display = (
        'monster_id_str',
        'pokemon_ep_url_plain',
        'pokemon_species_ep_url_plain',
        'pokemon_form_ep_url_plain',
    )
    ordering = ('monster_id_str',)
    raw_id_fields = ('pokemon', 'pokemon_species', 'pokemon_form',)
    readonly_fields = (
        'pokemon_ep_url',
        'pokemon_species_ep_url',
        'pokemon_form_ep_url',
    )
    fieldsets = (
        (None, {
            'fields': (
                'monster_id_str',
                'pokemon_ep_url',
                'pokemon_species_ep_url',
                'pokemon_form_ep_url',
                "pokemon_short_json",
                "pokemon_species_short_json",
                "pokemon_form_short_json",
            )
        }),
    )
    formfield_overrides = {
        JSONField: {
            'widget': JSONEditorWidget(
                options={'mode': 'form'},
                attrs={'style': 'width: 85%; height: 600px;'}
            )
        },
    }

    # 共通処理: プレフィックスを取り除き、末尾のスラッシュを削除し、ゼロ埋めする
    def _build_display(self, related, prefix):
        return related.ep_url.replace(prefix, "").strip("/").zfill(5)

    # 共通処理: 管理画面の変更ページへのリンクを生成（同じタブで開く）
    def _build_link(self, related, prefix):
        change_url = reverse(
            "admin:%s_%s_change" % (related._meta.app_label, related._meta.model_name),
            args=[related.pk]
        )
        display_text = self._build_display(related, prefix)
        return mark_safe(f'<a href="{change_url}">{display_text}</a>')

    # --- 一覧画面表示（プレーンテキスト） ---
    def pokemon_ep_url_plain(self, obj):
        return self._build_display(obj.pokemon, "https://pokeapi.co/api/v2/pokemon/")
    pokemon_ep_url_plain.short_description = 'Pokemon'

    def pokemon_species_ep_url_plain(self, obj):
        return self._build_display(obj.pokemon_species, "https://pokeapi.co/api/v2/pokemon-species/")
    pokemon_species_ep_url_plain.short_description = 'Pokemon Species'

    def pokemon_form_ep_url_plain(self, obj):
        return self._build_display(obj.pokemon_form, "https://pokeapi.co/api/v2/pokemon-form/")
    pokemon_form_ep_url_plain.short_description = 'Pokemon Form'

    # --- 詳細画面表示（クリック可能なリンク） ---
    def pokemon_ep_url(self, obj):
        return self._build_link(obj.pokemon, "https://pokeapi.co/api/v2/pokemon/")
    pokemon_ep_url.short_description = 'Pokemon'

    def pokemon_species_ep_url(self, obj):
        return self._build_link(obj.pokemon_species, "https://pokeapi.co/api/v2/pokemon-species/")
    pokemon_species_ep_url.short_description = 'Pokemon Species'

    def pokemon_form_ep_url(self, obj):
        return self._build_link(obj.pokemon_form, "https://pokeapi.co/api/v2/pokemon-form/")
    pokemon_form_ep_url.short_description = 'Pokemon Form'

@admin.register(S6_ProcessedPokemon)
class ProcessedPokemonAdmin(admin.ModelAdmin):
    list_display = (
        'monster_id_int',
        'monster_name_jp',
        'monster_name',
        'form_name',
        'form_name_jp',
        'front_url_exist',
    )
    search_fields = ('monster_name', 'monster_name_jp', 'form_name', 'form_name_jp')
    ordering = ('monster_id_int',)