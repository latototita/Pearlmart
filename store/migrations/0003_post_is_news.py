# Generated by Django 2.2 on 2022-06-21 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_category_is_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_news',
            field=models.BooleanField(default=False),
        ),
    ]
