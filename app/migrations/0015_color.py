# Generated by Django 3.2.22 on 2024-08-01 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20240730_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50)),
                ('color_css', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
            ],
        ),
    ]
