# Generated by Django 3.0.8 on 2020-08-05 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20200804_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='time_posted',
            field=models.DateField(auto_now=True),
        ),
    ]
