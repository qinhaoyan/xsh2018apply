# Generated by Django 2.0.1 on 2018-10-04 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20181004_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='asp',
            name='name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
