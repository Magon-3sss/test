# Generated by Django 3.2.22 on 2024-08-28 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20240828_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new_oper_tables',
            name='outil',
        ),
        migrations.AddField(
            model_name='new_oper_tables',
            name='outils',
            field=models.ManyToManyField(blank=True, to='app.TypeOutilsAgricoles'),
        ),
    ]
