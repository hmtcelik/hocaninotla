# Generated by Django 3.2.9 on 2022-02-28 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0045_auto_20220228_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_body',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='reportcomment',
            name='report_body',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
