# Generated by Django 3.2.9 on 2022-01-24 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_faculty_uni_shortcut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='uni_shortcut',
            field=models.CharField(max_length=10),
        ),
    ]