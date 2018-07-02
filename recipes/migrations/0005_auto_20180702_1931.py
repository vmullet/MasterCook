# Generated by Django 2.0.6 on 2018-07-02 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20180701_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeskill',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='recipeskill',
            name='description_fr',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='recipeskill',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recipeskill',
            name='name_fr',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recipetype',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='recipetype',
            name='description_fr',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='recipetype',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recipetype',
            name='name_fr',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
