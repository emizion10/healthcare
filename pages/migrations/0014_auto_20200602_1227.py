# Generated by Django 2.1.5 on 2020-06-02 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_auto_20200602_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratory',
            name='services',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='laboratory',
            name='address',
            field=models.TextField(blank=True),
        ),
    ]
