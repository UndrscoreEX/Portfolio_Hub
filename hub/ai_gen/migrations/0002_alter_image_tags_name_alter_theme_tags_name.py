# Generated by Django 4.2.8 on 2023-12-22 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_gen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image_tags',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='theme_tags',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
