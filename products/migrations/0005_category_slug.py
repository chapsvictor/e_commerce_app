# Generated by Django 3.2.13 on 2022-09-29 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=200, null=True),
        ),
    ]
