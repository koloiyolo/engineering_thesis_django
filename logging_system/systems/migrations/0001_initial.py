# Generated by Django 5.1.1 on 2024-11-16 16:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.TextField(blank=True, null=True)),
                ('host', models.TextField(blank=True, null=True)),
                ('program', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('label', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('ip', models.TextField(max_length=50)),
                ('system_type', models.IntegerField(choices=[(0, 'Device'), (1, 'Service')], default=0)),
                ('port', models.TextField(blank=True, max_length=50, null=True)),
                ('to_ping', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True)),
                ('last_ping', models.TextField(max_length=50, null=True)),
                ('last_log', models.TextField(max_length=50)),
                ('d_count', models.IntegerField(default=0)),
                ('email_notify', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('service_type', models.TextField(max_length=50)),
                ('model', models.TextField(blank=True, max_length=50, null=True)),
                ('notes', models.TextField(blank=True, max_length=256, null=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.location')),
            ],
        ),
        migrations.CreateModel(
            name='Ping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('ping', models.IntegerField(null=True)),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.system')),
            ],
        ),
    ]
