# Generated by Django 3.2.22 on 2024-09-13 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20240913_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_oper_tables',
            name='date_debut',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='new_oper_tables',
            name='date_fin',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
