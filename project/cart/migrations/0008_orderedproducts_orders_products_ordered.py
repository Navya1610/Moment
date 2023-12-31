# Generated by Django 4.2.2 on 2023-08-17 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appauth', '0002_remove_product_quantity'),
        ('cart', '0007_remove_orders_order_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.orders')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appauth.product')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='products_ordered',
            field=models.ManyToManyField(through='cart.OrderedProducts', to='appauth.product'),
        ),
    ]
