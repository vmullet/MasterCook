# Generated by Django 2.0.6 on 2018-06-24 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='thumbnail',
            field=models.ImageField(blank=True, default='default/default_ingredient.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='ingredienttype',
            name='thumbnail',
            field=models.ImageField(blank=True, default='default/default_ingredient_type.png', upload_to=''),
        ),
    ]
