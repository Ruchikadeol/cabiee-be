# Generated by Django 5.2.2 on 2025-06-09 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_remove_employee_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='shift_timings',
            field=models.CharField(blank=True, default='9am-6pm', null=True),
        ),
    ]
