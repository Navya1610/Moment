# Generated by Django 4.2.1 on 2023-09-11 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0025_cart_coupon_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='coupon_id',
            new_name='coupon',
        ),
    ]
