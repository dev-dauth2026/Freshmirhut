# Generated by Django 3.1.3 on 2021-05-24 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fresh', '0026_notice_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='count',
        ),
    ]
