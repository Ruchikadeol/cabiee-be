# Generated by Django 5.2.2 on 2025-06-26 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0006_driver_beneficiary_id_alter_driver_bank_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='beneficiary_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
