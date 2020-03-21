# Generated by Django 2.1.3 on 2020-03-21 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'patient'), (2, 'doctor'), (3, 'hospital'), (4, 'admin')], default=4)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('regid', models.CharField(max_length=60, unique=True)),
                ('dname', models.CharField(max_length=50)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.IntegerField(blank=True, choices=[(0, 'male'), (1, 'female'), (2, 'not specified')])),
                ('spec', models.CharField(blank=True, max_length=50)),
                ('hos', models.CharField(blank=True, max_length=150)),
                ('imagefile', models.ImageField(blank=True, default='default.jpg', upload_to='doctor/')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('regid', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(blank=True, max_length=10)),
                ('spec', models.TextField(blank=True)),
                ('services', models.TextField(blank=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('url', models.URLField(blank=True)),
                ('imagefile', models.ImageField(blank=True, upload_to='hospital/')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('regid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('pname', models.CharField(max_length=50)),
                ('gender', models.IntegerField(blank=True, choices=[(0, 'male'), (1, 'female'), (2, 'not specified')])),
                ('dob', models.DateField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('bloodgroup', models.CharField(blank=True, choices=[('apos', 'A+'), ('aneg', 'A-'), ('bpos', 'B+'), ('bneg', 'B-'), ('opos', 'O+'), ('oneg', 'O-'), ('abpos', 'AB+'), ('abneg', 'AB-'), ('unspecified', '-')], default='-', max_length=12)),
                ('place', models.CharField(blank=True, max_length=50)),
                ('imagefile', models.ImageField(blank=True, default='default.jpg', upload_to='patient/')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]