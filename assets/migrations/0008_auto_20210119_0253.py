# Generated by Django 2.2.17 on 2021-01-19 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_auto_20210119_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='assetIds',
            field=models.CharField(default=[], max_length=128, verbose_name='设备列'),
        ),
    ]
