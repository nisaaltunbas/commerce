# Generated by Django 5.0.6 on 2024-05-30 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_bid_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.FloatField(default=0),
        ),
    ]
