# Generated by Django 3.2.9 on 2022-02-24 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0037_comment_net_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='net_like',
        ),
    ]