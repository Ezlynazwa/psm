# Generated by Django 5.1.4 on 2025-05-26 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_customer_loyalty_points_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='customer_photo/'),
        ),
    ]
