# Generated by Django 3.2.15 on 2022-12-05 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0021_auto_20221202_1508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result_studentscall',
            old_name='results',
            new_name='result',
        ),
        migrations.AlterField(
            model_name='result_studentscall',
            name='joint_call',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='calls.studentscall'),
        ),
    ]