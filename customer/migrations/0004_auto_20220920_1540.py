# Generated by Django 3.2.13 on 2022-09-20 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0003_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='status',
            new_name='aprroval_status',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
        migrations.AddField(
            model_name='cart',
            name='orders',
            field=models.ManyToManyField(to='customer.OrderItem'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order_id',
            field=models.CharField(blank=True, max_length=20, verbose_name='order id'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='ordered_status',
            field=models.BooleanField(default=False, max_length=100, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
