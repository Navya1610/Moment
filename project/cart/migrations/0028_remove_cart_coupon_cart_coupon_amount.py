# Generated by Django 4.2.1 on 2023-09-11 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0027_alter_usercoupon_coupon_applied'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='coupon',
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
