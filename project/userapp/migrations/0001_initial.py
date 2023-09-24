# Generated by Django 4.2.1 on 2023-09-05 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0019_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_reason', models.TextField()),
                ('return_status', models.CharField(choices=[('Requested', 'Requested'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Processing', 'Processing'), ('Completed', 'Completed')], default='Requested', max_length=20)),
                ('return_request_date', models.DateTimeField(auto_now_add=True)),
                ('return_approval_date', models.DateTimeField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.orders')),
            ],
        ),
    ]
