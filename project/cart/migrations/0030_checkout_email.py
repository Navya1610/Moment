# Generated by Django 4.2.1 on 2023-09-12 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0029_remove_cart_coupon_amount_cartitem_coupon_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='email',
            field=models.CharField(default='default@example.com', max_length=30),
        ),
    ]
