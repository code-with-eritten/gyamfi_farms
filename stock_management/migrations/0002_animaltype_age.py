# Generated by Django 5.1.7 on 2025-03-30 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='animaltype',
            name='age',
            field=models.PositiveIntegerField(default=3),
            preserve_default=False,
        ),
    ]
