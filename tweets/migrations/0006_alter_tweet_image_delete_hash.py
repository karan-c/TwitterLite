# Generated by Django 3.2.8 on 2022-01-13 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_auto_20220113_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='image_delete_hash',
            field=models.CharField(max_length=50, null=True),
        ),
    ]