# Generated by Django 3.1.4 on 2020-12-23 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20201223_2254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.CharField(choices=[('breakfast', 'Завтрак'), ('lunch', 'Обед'), ('dinner', 'Ужин')], default='breakfast', max_length=50, verbose_name='Тег'),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
