# Generated by Django 5.1.4 on 2025-02-05 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='subsribe',
            new_name='subscribe',
        ),
    ]
