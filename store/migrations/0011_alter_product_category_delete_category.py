# Generated by Django 5.1.4 on 2025-01-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_category_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
