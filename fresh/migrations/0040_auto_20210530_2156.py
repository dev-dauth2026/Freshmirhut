# Generated by Django 3.1.3 on 2021-05-30 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fresh', '0039_auto_20210530_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesscontact',
            name='location_address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
