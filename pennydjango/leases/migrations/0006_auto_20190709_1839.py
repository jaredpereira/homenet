# Generated by Django 2.2.3 on 2019-07-09 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leases', '0005_rentalapplication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentalapplication',
            old_name='status',
            new_name='completed',
        ),
    ]
