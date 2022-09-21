# Generated by Django 3.2.13 on 2022-09-20 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_checked_out', models.BooleanField(default=False, verbose_name='checked_out')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=20, verbose_name='order id')),
                ('quantity', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('pending', 'Pending Confirmation'), ('approved', 'Approved'), ('declined', 'Declined'), ('customer_cancelled', 'Customer Cancelled')], default='pending', max_length=100)),
                ('is_paid', models.BooleanField(default=False, verbose_name='is paid')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('pickup_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(choices=[('pending', 'Pending Confirmation'), ('approved', 'Approved'), ('declined', 'Declined'), ('customer_cancelled', 'Customer Cancelled')], default='pending', max_length=100)),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='customer.order')),
            ],
        ),
    ]