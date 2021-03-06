# Generated by Django 3.0.2 on 2020-02-27 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('c2shiptrack', '0012_auto_20200223_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lokasi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(blank=True, max_length=32, null=True)),
                ('longitude', models.CharField(blank=True, max_length=32, null=True)),
                ('password', models.CharField(blank=True, max_length=32, null=True)),
                ('lokasi', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nama', models.CharField(blank=True, max_length=32, null=True)),
                ('username', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=32, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('lokasi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='c2shiptrack.Lokasi')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
