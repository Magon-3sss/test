# Generated by Django 3.2.22 on 2024-09-19 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_rename_rechangepiece_rechangepiecee'),
    ]

    operations = [
        migrations.CreateModel(
            name='RechangePieces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_pieces', models.CharField(max_length=100)),
                ('type_pieces', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.typepieces')),
            ],
        ),
        migrations.DeleteModel(
            name='RechangePiecee',
        ),
        migrations.AlterField(
            model_name='new_oper_tables',
            name='pieces',
            field=models.ManyToManyField(related_name='operations', to='app.RechangePieces'),
        ),
    ]