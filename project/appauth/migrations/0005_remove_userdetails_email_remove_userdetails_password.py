# Generated by Django 4.2.1 on 2023-08-25 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appauth', '0004_alter_userdetails_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='password',
        ),
    ]