# Generated by Django 3.0.3 on 2020-06-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20200618_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='status',
            field=models.CharField(default='Not Published', max_length=200),
        ),
    ]
