# Generated by Django 3.1.1 on 2020-09-12 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20200913_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='questions_attempted',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
