# Generated by Django 3.1.5 on 2021-01-19 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='affiliation',
            field=models.CharField(default='', help_text='To which institute are you affiliated?', max_length=128),
        ),
    ]
