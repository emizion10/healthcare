# Generated by Django 2.1.5 on 2020-06-02 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_auto_20200601_2108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('regid', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('contact', models.CharField(blank=True, max_length=14)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='hospital',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='hospital',
            name='contact',
            field=models.CharField(blank=True, max_length=14),
        ),
        migrations.AddField(
            model_name='hospital',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='place',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
