# Generated by Django 2.2.3 on 2019-07-10 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leases', '0008_rentalapplication_editing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lease',
            name='status',
            field=models.CharField(choices=[('awaiting_deposit', 'Awaiting Deposit'), ('unsigned_unapproved', 'Unsigned, Unapproved'), ('unsigned_approved', 'Unsigned, Approved'), ('signed_approved', 'Signed, Approved'), ('client_backed_out', 'Client Backed Out'), ('cancelled', 'Cancelled'), ('awaiting_op', 'Awaiting OP'), ('pending_deletion', 'Pending Deletion')], default='awaiting_deposit', max_length=50),
        ),
    ]
