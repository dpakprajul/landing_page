# Generated by Django 4.2.5 on 2023-09-11 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='number',
            field=models.IntegerField(default=22),
            preserve_default=False,
        ),
    ]