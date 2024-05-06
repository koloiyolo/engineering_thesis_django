# Generated by Django 5.0.4 on 2024-05-06 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_dataset_clusters'),
    ]

    operations = [
        migrations.CreateModel(
            name='MlModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('model_type', models.TextField(max_length=50)),
                ('args', models.TextField(max_length=200)),
                ('accuracy', models.TextField(max_length=10)),
                ('dataset_id', models.TextField(max_length=20)),
                ('file', models.BinaryField()),
            ],
        ),
    ]
