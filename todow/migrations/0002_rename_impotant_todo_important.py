# Generated by Django 4.1.5 on 2023-01-05 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todow', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='impotant',
            new_name='important',
        ),
    ]