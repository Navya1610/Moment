# Generated by Django 4.2.1 on 2023-09-11 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0028_remove_cart_coupon_cart_coupon_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='coupon_amount',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='coupon_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
