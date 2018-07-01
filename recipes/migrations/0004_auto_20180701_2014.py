# Generated by Django 2.0.6 on 2018-07-01 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20180701_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reciperate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to=settings.AUTH_USER_MODEL),
        ),
    ]
