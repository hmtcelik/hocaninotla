# Generated by Django 3.2.9 on 2022-03-02 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0048_doctor_doctor_lecture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doctor_lecture',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='doctor_link',
            field=models.URLField(blank=True),
        ),
    ]
