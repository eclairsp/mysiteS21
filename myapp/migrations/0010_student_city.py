# Generated by Django 3.2.3 on 2021-08-07 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20210807_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='city',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]