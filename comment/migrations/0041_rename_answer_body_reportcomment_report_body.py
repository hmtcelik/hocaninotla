# Generated by Django 3.2.9 on 2022-02-28 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0040_auto_20220228_1101'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportcomment',
            old_name='answer_body',
            new_name='report_body',
        ),
    ]