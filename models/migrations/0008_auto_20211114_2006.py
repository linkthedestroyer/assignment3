# Generated by Django 3.2.8 on 2021-11-15 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0007_auto_20211113_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan_request',
            name='loan_request_status',
            field=models.CharField(choices=[('REQUESTED', 'Requested'), ('ACCEPTED', 'Accepted'), ('DECLINED', 'Declined'), ('RECALLED', 'Recalled'), ('RETURNED', 'Returned')], default='REQUESTED', max_length=50),
        ),
        migrations.AlterField(
            model_name='loaned_card',
            name='card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='models.card'),
        ),
    ]
