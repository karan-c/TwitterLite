# Generated by Django 3.2.8 on 2021-12-27 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='retweet_count',
            field=models.IntegerField(default=0),
        ),
    ]
