# Generated by Django 4.1.2 on 2022-11-08 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0003_remove_jointcall_timeline_timeline_joint_call'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='name')),
                ('annex', models.FileField(blank=True, null=True, upload_to='uploads/calls_internal', verbose_name='annex')),
                ('joint_call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annex', to='calls.jointcall')),
            ],
        ),
    ]