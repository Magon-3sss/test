# Generated by Django 3.2.22 on 2024-09-03 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20240828_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='RechangePiece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_pieces', models.CharField(max_length=100)),
                ('nombre_de_pieces', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='new_oper_tables',
            name='nombre_de_pieces',
        ),
        migrations.RemoveField(
            model_name='new_oper_tables',
            name='outil',
        ),
        migrations.RemoveField(
            model_name='new_oper_tables',
            name='type_pieces',
        ),
        migrations.AddField(
            model_name='new_oper_tables',
            name='outils',
            field=models.ManyToManyField(related_name='form', to='app.Tool'),
        ),
        migrations.AddField(
            model_name='new_oper_tables',
            name='pieces',
            field=models.ManyToManyField(related_name='operations', to='app.RechangePiece'),
        ),
    ]