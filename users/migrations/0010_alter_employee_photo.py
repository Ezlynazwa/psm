# Generated by Django 5.1.4 on 2025-05-22 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='employee_photo/'),
        ),
    ]
