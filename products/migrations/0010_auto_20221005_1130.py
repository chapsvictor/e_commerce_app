# Generated by Django 3.2.13 on 2022-10-05 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20221005_0817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='products.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='colour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colour', to='products.colour'),
        ),
    ]