# Generated by Django 5.1.3 on 2024-12-10 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_director_alter_comment_options_alter_genre_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время публикации'),
        ),
    ]