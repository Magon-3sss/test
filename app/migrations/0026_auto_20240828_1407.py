# Generated by Django 3.2.22 on 2024-08-28 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20240828_1320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new_oper_tables',
            name='outils',
        ),
        migrations.AddField(
            model_name='new_oper_tables',
            name='outil',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
