# Generated by Django 4.2.11 on 2024-05-02 20:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_blog_image_alter_blog_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 5, 2, 23, 26, 24, 969238), verbose_name='Опубликована'),
        ),
    ]
