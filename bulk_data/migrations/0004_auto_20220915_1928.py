# Generated by Django 3.2.15 on 2022-09-15 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulk_data', '0003_auto_20220915_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databasesbulk',
            name='bulk_Patent',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Patents'),
        ),
        migrations.AlterField(
            model_name='databasesbulk',
            name='bulk_Professor',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Professors'),
        ),
        migrations.AlterField(
            model_name='databasesbulk',
            name='bulk_ResearchGroup',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Research groups'),
        ),
    ]