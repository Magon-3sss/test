# Generated by Django 3.2.22 on 2024-09-09 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_remove_mapform_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_oper_tables',
            name='coordinates',
            field=models.ManyToManyField(related_name='operations', to='app.Marker'),
        ),
    ]