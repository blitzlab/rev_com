# Generated by Django 3.0.3 on 2020-07-27 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0004_image_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='status',
            field=models.CharField(blank=True, default='Pending', max_length=100, null=True),
        ),
    ]
