# Generated by Django 4.1 on 2022-09-01 00:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="researchgroup",
            old_name="cod_hermes",
            new_name="hermes_code",
        ),
        migrations.RenameField(
            model_name="researchgroup",
            old_name="cod_minciencias",
            new_name="minciencias_code",
        ),
    ]
