# Generated by Django 3.2 on 2022-07-18 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20220717_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='name',
            new_name='key',
        ),
    ]
