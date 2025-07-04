# Generated by Django 5.1.4 on 2025-06-02 19:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0040_productrecommendation_alter_product_options_and_more'),
        ('users', '0013_customerprofile_skinassessment_somemodel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrecommendation',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customerprofile'),
        ),
        migrations.AddField(
            model_name='productrecommendation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='recommended_for',
            field=models.ManyToManyField(through='store.ProductRecommendation', to='users.customerprofile'),
        ),
        migrations.AlterUniqueTogether(
            name='productrecommendation',
            unique_together={('product', 'customer')},
        ),
    ]
