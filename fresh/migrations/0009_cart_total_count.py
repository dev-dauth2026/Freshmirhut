# Generated by Django 3.1.3 on 2021-05-21 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fresh', '0008_product_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
