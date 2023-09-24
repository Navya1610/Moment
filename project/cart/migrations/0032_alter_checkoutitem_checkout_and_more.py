# Generated by Django 4.2.1 on 2023-09-14 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appauth', '0007_userdetails_email'),
        ('cart', '0031_delete_discount_rename_max_amount_coupon_min_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutitem',
            name='checkout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appauth.userdetails'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='billing_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_orders', to='appauth.userdetails'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='shipping_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_orders', to='appauth.userdetails'),
        ),
    ]
