# Generated by Django 3.0.3 on 2020-06-11 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_premiumuserreferupgradebonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]