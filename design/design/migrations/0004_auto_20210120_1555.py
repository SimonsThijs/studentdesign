# Generated by Django 3.1.5 on 2021-01-20 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0003_auto_20210119_1703'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
