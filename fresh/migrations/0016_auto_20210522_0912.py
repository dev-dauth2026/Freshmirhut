# Generated by Django 3.1.3 on 2021-05-21 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fresh', '0015_cartproduct_c_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
