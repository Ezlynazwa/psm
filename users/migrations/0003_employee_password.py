# Generated by Django 5.1.4 on 2025-01-15 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_employee_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='password',
            field=models.CharField(default='defaultpassword', max_length=128),
        ),
    ]
