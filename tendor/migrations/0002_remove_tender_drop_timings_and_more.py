# Generated by Django 5.2.2 on 2025-06-08 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0001_initial'),
        ('group', '0003_remove_group_employees_remove_group_monthly_rental_and_more'),
        ('tendor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tender',
            name='drop_timings',
        ),
        migrations.RemoveField(
            model_name='tender',
            name='location_details',
        ),
        migrations.RemoveField(
            model_name='tender',
            name='pickup_timings',
        ),
        migrations.AddField(
            model_name='tender',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver_tender', to='driver.driver'),
        ),
        migrations.AddField(
            model_name='tender',
            name='drop_location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tender',
            name='pickup_location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='tender',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_tender', to='group.group'),
        ),
    ]
