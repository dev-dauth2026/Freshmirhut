# Generated by Django 3.1.3 on 2021-06-07 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fresh', '0055_remove_savedproduct_kg_quantity'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Save',
            new_name='Saved',
        ),
        migrations.RenameField(
            model_name='savedproduct',
            old_name='save',
            new_name='saved',
        ),
    ]