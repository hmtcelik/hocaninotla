# Generated by Django 3.2.9 on 2022-03-02 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0047_remove_doctor_scholar_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='doctor_lecture',
            field=models.CharField(default='default', max_length=150),
        ),
    ]