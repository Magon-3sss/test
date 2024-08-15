# Generated by Django 3.2.22 on 2024-08-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_descriptionfiltre'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnomalyPalmier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('traitement', models.CharField(max_length=500)),
                ('symptomes', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='AnomalyPommeDeTerre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('traitement', models.CharField(max_length=500)),
                ('symptomes', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriesPlantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_plante', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SousCategoriesOlives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_plante', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SousCategoriesPalmier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_plante', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SousCategoriesPommeDeTerre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_plante', models.CharField(max_length=50)),
            ],
        ),
    ]
