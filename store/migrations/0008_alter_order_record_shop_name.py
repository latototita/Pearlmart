# Generated by Django 3.2 on 2022-07-18 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_order_record_ordering_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_record',
            name='shop_name',
            field=models.CharField(default='', max_length=60),
        ),
    ]