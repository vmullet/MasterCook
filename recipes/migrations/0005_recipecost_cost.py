# Generated by Django 2.0.6 on 2018-06-25 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20180625_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipecost',
            name='cost',
            field=models.FloatField(default=0.0),
        ),
    ]
