# Generated by Django 4.2.1 on 2023-09-15 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0035_alter_orders_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='cartitem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.cartitem'),
        ),
    ]