# Generated by Django 5.1.4 on 2025-01-30 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_qr_code', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcodes',
            name='image',
            field=models.ImageField(default='none', upload_to=''),
        ),
        migrations.AlterField(
            model_name='qrcodes',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
