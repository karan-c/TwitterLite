# Generated by Django 3.2.8 on 2021-11-03 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0006_auto_20211102_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='retweet_obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tweets.tweet'),
        ),
    ]