# Generated by Django 2.0.6 on 2018-06-25 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20180625_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_cost',
        ),
        migrations.AddField(
            model_name='recipecost',
            name='recipe',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe'),
        ),
    ]