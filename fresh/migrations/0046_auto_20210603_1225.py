# Generated by Django 3.1.3 on 2021-06-03 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fresh', '0045_remove_businesscontact_location_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesscontact',
            name='location_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='businesscontact',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
    ]
