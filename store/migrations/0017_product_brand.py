# Generated by Django 5.1.4 on 2025-05-15 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_product_images_productimage_productvariation'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default='Brand', max_length=100),
        ),
    ]
