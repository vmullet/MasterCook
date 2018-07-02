# Generated by Django 2.0.6 on 2018-07-02 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('name_fr', models.CharField(max_length=100, null=True)),
                ('css_class', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('name_en', models.CharField(max_length=10, null=True)),
                ('name_fr', models.CharField(max_length=10, null=True)),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UnitMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('name_en', models.CharField(max_length=15, null=True)),
                ('name_fr', models.CharField(max_length=15, null=True)),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
    ]
