# Generated by Django 3.2.9 on 2021-11-07 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0004_auto_20211106_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_cost',
            field=models.CharField(blank=True, default=' ', max_length=20, null=True),
        ),
    ]
