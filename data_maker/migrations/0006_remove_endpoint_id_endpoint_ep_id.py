# Generated by Django 5.1.6 on 2025-03-18 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_maker', '0005_pokemonformrawdata_pokemonspeciesrawdata_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endpoint',
            name='id',
        ),
        migrations.AddField(
            model_name='endpoint',
            name='ep_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
