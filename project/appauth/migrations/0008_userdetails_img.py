# Generated by Django 4.2.1 on 2023-09-19 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appauth', '0007_userdetails_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='img/'),
        ),
    ]
