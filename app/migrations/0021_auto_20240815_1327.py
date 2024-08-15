# Generated by Django 3.2.22 on 2024-08-15 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_anomalypalmier_anomalypommedeterre_categoriesplantes_souscategoriesolives_souscategoriespalmier_sous'),
    ]

    operations = [
        migrations.RenameField(
            model_name='souscategoriesolives',
            old_name='nom_plante',
            new_name='nom_souscategorie_olive',
        ),
        migrations.RenameField(
            model_name='souscategoriespalmier',
            old_name='nom_plante',
            new_name='nom_souscategorie_palmier',
        ),
        migrations.RenameField(
            model_name='souscategoriespommedeterre',
            old_name='nom_plante',
            new_name='nom_souscategorie_pomme_terre',
        ),
    ]
