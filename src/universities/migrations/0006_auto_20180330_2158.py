# Generated by Django 2.1.dev20180328172503 on 2018-03-30 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0005_university_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
