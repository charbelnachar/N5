# Generated by Django 3.2.10 on 2024-06-26 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('identifier', models.CharField(max_length=20, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(max_length=20, unique=True)),
                ('brand', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=30)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='app.person')),
            ],
        ),
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('comments', models.TextField()),
                ('officer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.officer')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='violations', to='app.vehicle')),
            ],
        ),
    ]