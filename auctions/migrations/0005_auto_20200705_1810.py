# Generated by Django 3.0.8 on 2020-07-06 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200705_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='aution',
            new_name='auction',
        ),
    ]