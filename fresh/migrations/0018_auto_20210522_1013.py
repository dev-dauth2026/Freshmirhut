# Generated by Django 3.1.3 on 2021-05-22 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fresh', '0017_auto_20210522_0914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='c_count',
        ),
        migrations.RemoveField(
            model_name='product',
            name='count',
        ),
    ]