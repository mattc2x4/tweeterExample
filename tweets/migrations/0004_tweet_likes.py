# Generated by Django 3.1.2 on 2020-11-03 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0003_tweet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
