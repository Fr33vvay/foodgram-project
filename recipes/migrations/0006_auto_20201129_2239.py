# Generated by Django 3.1.3 on 2020-11-29 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20201129_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='dimension',
            field=models.CharField(max_length=50, verbose_name='Единицы измерения'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='Картинка'),
        ),
    ]
