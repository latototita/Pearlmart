# Generated by Django 3.2 on 2022-07-17 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20220716_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='alternative_Phone',
            field=models.CharField(blank=True, default='1', max_length=13),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone',
            field=models.CharField(blank=True, default='1', max_length=13),
        ),
    ]