# Generated by Django 3.1.3 on 2020-11-25 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userauthkey',
            name='reset_password_key',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
