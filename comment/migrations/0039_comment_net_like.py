# Generated by Django 3.2.9 on 2022-02-24 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0038_remove_comment_net_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='net_like',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
