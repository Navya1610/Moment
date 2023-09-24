# Generated by Django 4.2.1 on 2023-09-05 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0021_alter_orders_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedproducts',
            name='product_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Out for Shipping', 'Out for Shipping'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=20),
        ),
    ]
