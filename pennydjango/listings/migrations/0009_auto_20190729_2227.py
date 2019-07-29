# Generated by Django 2.2.3 on 2019-07-29 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_auto_20190724_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('approved', 'Approved'), ('cancelled', 'Cancelled'), ('rented', 'Rented')], default='draft', max_length=50),
        ),
    ]