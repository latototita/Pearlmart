# Generated by Django 3.2 on 2022-07-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_order_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='shop',
            field=models.CharField(blank=True, default=1, max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='shop',
            field=models.CharField(blank=True, default=1, max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='Uploads/products/'),
        ),
    ]
