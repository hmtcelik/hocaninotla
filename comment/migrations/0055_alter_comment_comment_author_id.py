# Generated by Django 3.2.9 on 2022-03-08 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0054_comment_comment_author_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_author_id',
            field=models.IntegerField(),
        ),
    ]
