# Generated by Django 4.2.1 on 2023-08-25 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_checkout_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_coupon_applied',
            field=models.BooleanField(default=False),
        ),
    ]