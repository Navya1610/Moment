# Generated by Django 4.2.1 on 2023-08-10 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appauth', '0002_remove_product_quantity'),
        ('cart', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appauth.variants'),
        ),
    ]