# Generated by Django 3.0.4 on 2020-03-28 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200328_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='mean_stars',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]
