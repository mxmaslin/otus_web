# Generated by Django 2.2.12 on 2020-06-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20200618_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_zip',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
