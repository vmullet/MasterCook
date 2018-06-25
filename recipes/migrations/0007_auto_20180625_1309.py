# Generated by Django 2.0.6 on 2018-06-25 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_reciperate_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipecost',
            name='recipe',
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_cost',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='recipes.RecipeCost'),
        ),
    ]
