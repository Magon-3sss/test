# Generated by Django 3.2.22 on 2024-07-30 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_filtreevolution_filtrefertilisation_filtrehumidite_filtreirrigation_filtremaladie'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Filtre',
            new_name='FiltreVegitation',
        ),
    ]