# Generated by Django 5.0.3 on 2024-05-01 08:38

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_blog_author_alter_blog_posted'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 5, 1, 11, 38, 12, 184472), verbose_name='Опубликована'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('posted', models.DateTimeField(db_index=True, default=datetime.datetime(2024, 5, 1, 11, 38, 12, 185472), verbose_name='Опубликован')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'db_table': 'Comments',
                'ordering': ['-posted'],
            },
        ),
    ]
