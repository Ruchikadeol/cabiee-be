# Generated by Django 5.2.2 on 2025-06-12 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_rename_is_active_groupempoyeemapping_is_active_member'),
        ('group', '0006_grouphistory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GroupEmpoyeeMapping',
            new_name='GroupEmployeeMapping',
        ),
    ]
