# Generated by Django 3.2.15 on 2022-08-21 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research_groups', '0008_auto_20220819_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchgroup',
            name='category',
            field=models.CharField(choices=[('cat_01', 'A'), ('cat_02', 'A1'), ('cat_03', 'A2'), ('cat_04', 'B'), ('cat_05', 'C'), ('cat_06', 'No reconcido')], max_length=6),
        ),
    ]
