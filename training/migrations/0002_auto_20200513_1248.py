# Generated by Django 3.0.6 on 2020-05-13 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='duration',
            field=models.DurationField(verbose_name='duration'),
        ),
    ]