# Generated by Django 3.2.5 on 2021-08-24 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('towingapp', '0005_alter_clock_in_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clock_in',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
