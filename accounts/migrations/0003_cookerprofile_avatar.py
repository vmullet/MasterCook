# Generated by Django 2.0.6 on 2018-06-22 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180622_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookerprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='default_avatar.png', upload_to=''),
        ),
    ]
