# Generated by Django 3.2.13 on 2022-09-23 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_auto_20220922_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='orders',
            field=models.ManyToManyField(blank=True, to='customer.OrderItem'),
        ),
    ]