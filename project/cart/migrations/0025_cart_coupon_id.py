# Generated by Django 4.2.1 on 2023-09-11 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0024_orders_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.coupon'),
        ),
    ]
