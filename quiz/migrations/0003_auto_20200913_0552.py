# Generated by Django 3.1.1 on 2020-09-12 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='correct_answer',
            new_name='correct_option',
        ),
    ]
