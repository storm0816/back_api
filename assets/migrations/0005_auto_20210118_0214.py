# Generated by Django 2.2.17 on 2021-01-18 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_auto_20210115_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='域名'),
        ),
    ]
