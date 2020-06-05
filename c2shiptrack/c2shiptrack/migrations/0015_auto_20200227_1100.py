# Generated by Django 3.0.2 on 2020-02-27 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('c2shiptrack', '0014_auto_20200227_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='LokasiUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lokasi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='c2shiptrack.Lokasi')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lokasi_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]