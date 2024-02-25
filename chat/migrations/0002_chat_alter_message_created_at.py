# Generated by Django 5.0.2 on 2024-02-25 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
    ]