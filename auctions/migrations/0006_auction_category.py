# Generated by Django 3.0.8 on 2020-07-09 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200705_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
