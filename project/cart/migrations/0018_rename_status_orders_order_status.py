# Generated by Django 4.2.1 on 2023-09-02 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0017_rename_order_status_orders_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='status',
            new_name='order_status',
        ),
    ]
