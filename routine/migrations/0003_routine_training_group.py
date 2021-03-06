# Generated by Django 3.0.6 on 2020-05-24 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20200524_1555'),
        ('routine', '0002_auto_20200513_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='routine',
            name='training_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.TrainingGroup', verbose_name='training group'),
            preserve_default=False,
        ),
    ]
