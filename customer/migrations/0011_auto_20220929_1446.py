# Generated by Django 3.2.13 on 2022-09-29 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_alter_cart_orders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='Total_payment_price',
            new_name='total_payment_price',
        ),
        migrations.AlterField(
            model_name='cart',
            name='orders',
            field=models.ManyToManyField(blank=True, to='customer.OrderItem'),
        ),
    ]
