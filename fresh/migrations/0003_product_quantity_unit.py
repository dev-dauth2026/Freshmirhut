# Generated by Django 3.1.3 on 2021-05-15 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fresh', '0002_auto_20210516_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity_unit',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]