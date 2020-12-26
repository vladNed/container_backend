# Generated by Django 3.1.4 on 2020-12-26 20:40

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document_units', '0002_auto_20201226_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentformat',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterUniqueTogether(
            name='documentformat',
            unique_together=set(),
        ),
    ]