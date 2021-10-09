# Generated by Django 2.2.10 on 2021-10-09 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_name', models.CharField(default=' ', max_length=50)),
                ('card_status', models.CharField(choices=[('UNUSED', 'Unused'), ('IN_DECK', 'In Deck'), ('AVAILABLE_FOR_LOAN', 'Available for Loan'), ('LOANED_OUT', 'Loaned Out')], default='UNUSED', max_length=50)),
                ('card_rarity', models.CharField(default=' ', max_length=20)),
                ('card_set', models.CharField(default=' ', max_length=20)),
                ('card_cost', models.CharField(default=' ', max_length=20)),
                ('card_color', models.CharField(default=' ', max_length=20)),
                ('card_type', models.CharField(default=' ', max_length=50)),
                ('card_text', models.CharField(default=' ', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory_name', models.CharField(default=' ', max_length=50)),
                ('inventory_view_status', models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], default='PUBLIC', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Loan_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_request_status', models.CharField(choices=[('REQUESTED', 'Requested'), ('ACCEPTED', 'Accepted'), ('DECLINED', 'Declined')], default='REQUESTED', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Loaned_Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('returned_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loaned_Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loaned_inventory_name', models.CharField(default=' ', max_length=50)),
                ('loaned_inventory_view_status', models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], default='PUBLIC', max_length=50)),
            ],
        ),
    ]
