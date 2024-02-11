# Generated by Django 5.0.1 on 2024-02-11 11:20

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=100, validators=[core.validators.validate_not_empty_or_single_space]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=100, validators=[core.validators.validate_not_empty_or_single_space]),
        ),
    ]
