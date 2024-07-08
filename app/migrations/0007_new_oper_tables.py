# Generated by Django 3.2.22 on 2024-07-08 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_Oper_Tables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_rh', models.CharField(blank=True, max_length=50, null=True)),
                ('type_machine_engins', models.CharField(blank=True, max_length=50, null=True)),
                ('carburant', models.CharField(blank=True, max_length=100, null=True)),
                ('typeoperation', models.CharField(blank=True, max_length=100, null=True)),
                ('date_debut', models.CharField(blank=True, max_length=100, null=True)),
                ('date_fin', models.CharField(blank=True, max_length=100, null=True)),
                ('duree_utilisation_programme', models.CharField(blank=True, max_length=50, null=True)),
                ('quantite_carburant', models.CharField(blank=True, max_length=50, null=True)),
                ('outil', models.CharField(blank=True, max_length=50, null=True)),
                ('duree_utilisation', models.CharField(blank=True, max_length=50, null=True)),
                ('type_pieces', models.CharField(blank=True, max_length=50, null=True)),
                ('duree_utilisation_piece', models.CharField(blank=True, max_length=50, null=True)),
                ('type_graines_pousses', models.CharField(blank=True, max_length=50, null=True)),
                ('quantite_graine_utilisee', models.CharField(blank=True, max_length=50, null=True)),
                ('type_engrais', models.CharField(blank=True, max_length=50, null=True)),
                ('quantite_engrais_utilisee', models.CharField(blank=True, max_length=50, null=True)),
                ('type_traitement', models.CharField(blank=True, max_length=50, null=True)),
                ('quantite_traitement_utilisee', models.CharField(blank=True, max_length=50, null=True)),
                ('time', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
