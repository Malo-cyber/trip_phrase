# Generated by Django 4.0.5 on 2022-06-07 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phraseList', '0006_dicty_dicty_phrase_traductions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dicty',
            name='dicty',
        ),
    ]
