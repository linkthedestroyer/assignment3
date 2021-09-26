# Generated by Django 2.2.10 on 2021-09-26 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loaned_card',
            name='returned_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loaned_inventory',
            name='loaned_inventory_loanee_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Loanee', verbose_name='test'),
        ),
    ]
