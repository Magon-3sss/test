# Generated by Django 3.2.22 on 2024-09-09 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_new_oper_tables_coordinates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new_oper_tables',
            name='coordinates',
        ),
    ]
