# Generated by Django 4.2.1 on 2023-09-05 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0019_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Out for Shipping', 'Out for Shipping'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Returned', 'Returned')], default='Pending', max_length=20),
        ),
    ]
