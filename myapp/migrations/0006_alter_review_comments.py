# Generated by Django 3.2.3 on 2021-07-19 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
