# Generated by Django 5.1.4 on 2025-05-29 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_remove_order_order_id_product_finish_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='coverage',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='spf',
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
    ]
