# Generated by Django 5.1.4 on 2025-01-11 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
