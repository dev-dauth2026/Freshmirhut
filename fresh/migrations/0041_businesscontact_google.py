# Generated by Django 3.1.3 on 2021-05-30 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fresh', '0040_auto_20210530_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesscontact',
            name='google',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
