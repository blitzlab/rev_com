# Generated by Django 3.0.3 on 2020-06-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200611_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='PremiumUserCommentBonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
            ],
            options={
                'verbose_name_plural': 'Premium User Comment Bonus',
            },
        ),
    ]
