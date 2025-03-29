# Generated by Django 5.1.6 on 2025-03-19 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_maker', '0008_s3_monsterindividual'),
    ]

    operations = [
        migrations.RenameField(
            model_name='s3_monsterindividual',
            old_name='monster_id',
            new_name='monster_id_str',
        ),
        migrations.RenameField(
            model_name='s3_monsterindividual',
            old_name='pokemon_form',
            new_name='pokemon_form_raw_data',
        ),
        migrations.RenameField(
            model_name='s3_monsterindividual',
            old_name='pokemon',
            new_name='pokemon_raw_data',
        ),
        migrations.RenameField(
            model_name='s3_monsterindividual',
            old_name='pokemon_species',
            new_name='pokemon_species_raw_data',
        ),
    ]
