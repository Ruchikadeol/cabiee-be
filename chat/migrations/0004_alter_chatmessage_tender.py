# Generated by Django 5.2.2 on 2025-07-02 03:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_chatmessage_offer_alter_chatmessage_receiver_and_more'),
        ('tendor', '0018_alter_tender_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='tender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tender_message', to='tendor.tender'),
        ),
    ]
