# Generated by Django 3.2.22 on 2024-07-05 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_anomaly'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
                ('result_image', models.ImageField(blank=True, null=True, upload_to='assets/results/')),
            ],
        ),
    ]
