# Generated by Django 3.2.9 on 2022-02-21 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0028_remove_commentanswer_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='doctor_rate',
        ),
    ]