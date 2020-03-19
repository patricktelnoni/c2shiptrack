# Generated by Django 3.0.2 on 2020-02-23 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('c2shiptrack', '0003_loggedinuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggedinuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='SessionKey',
        ),
    ]
