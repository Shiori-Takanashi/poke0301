# Generated by Django 5.1.6 on 2025-03-22 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data_maker", "0023_rename_stats_a_s4_semifinalmonsterindividual_stat_a"),
    ]

    operations = [
        migrations.RenameField(
            model_name="s4_semifinalmonsterindividual",
            old_name="stats_b",
            new_name="stat_b",
        ),
        migrations.RenameField(
            model_name="s4_semifinalmonsterindividual",
            old_name="stats_c",
            new_name="stat_c",
        ),
        migrations.RenameField(
            model_name="s4_semifinalmonsterindividual",
            old_name="stats_d",
            new_name="stat_d",
        ),
        migrations.RenameField(
            model_name="s4_semifinalmonsterindividual",
            old_name="stats_h",
            new_name="stat_h",
        ),
        migrations.RenameField(
            model_name="s4_semifinalmonsterindividual",
            old_name="stats_s",
            new_name="stat_s",
        ),
    ]
