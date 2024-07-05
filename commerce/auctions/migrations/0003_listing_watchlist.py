# Generated by Django 5.0.6 on 2024-05-30 04:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='userWatchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
