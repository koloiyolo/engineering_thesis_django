# Generated by Django 5.1.1 on 2024-11-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
    ]
