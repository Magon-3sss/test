# Generated by Django 3.2.22 on 2024-07-26 09:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_uploadedimage_disease_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='anomaly',
            name='symptomes',
            field=models.CharField(default=django.utils.timezone.now, max_length=500),
            preserve_default=False,
        ),
    ]