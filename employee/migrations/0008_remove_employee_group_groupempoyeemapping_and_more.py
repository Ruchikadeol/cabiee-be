# Generated by Django 5.2.2 on 2025-06-12 04:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_alter_employee_address'),
        ('group', '0005_remove_group_employees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='group',
        ),
        migrations.CreateModel(
            name='GroupEmpoyeeMapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.group')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='group',
            field=models.ManyToManyField(related_name='employee', through='employee.GroupEmpoyeeMapping', to='employee.employee'),
        ),
    ]
