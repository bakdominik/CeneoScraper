# Generated by Django 3.0.4 on 2020-03-27 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200327_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='recomendation',
            field=models.BooleanField(null=True),
        ),
    ]