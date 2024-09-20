# Generated by Django 3.2.22 on 2024-09-19 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_auto_20240919_1743'),
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
        migrations.DeleteModel(
            name='RechangePieces',
        ),
        migrations.AlterField(
            model_name='new_oper_tables',
            name='pieces',
            field=models.ManyToManyField(related_name='operations', to='app.RechangePiece'),
        ),
    ]
