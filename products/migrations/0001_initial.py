# Generated by Django 3.2.13 on 2022-09-20 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=200)),
                ('price', models.IntegerField()),
                ('is_instock', models.BooleanField(default=True, verbose_name='in stock?')),
                ('product_in_stock_count', models.IntegerField(default=0, verbose_name='stock count')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/products/')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('product_id', models.CharField(blank=True, max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='products.category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['-date_created'],
            },
        ),
    ]
