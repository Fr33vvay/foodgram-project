# Generated by Django 3.1.4 on 2020-12-31 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_auto_20201231_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='slug',
        ),
    ]
