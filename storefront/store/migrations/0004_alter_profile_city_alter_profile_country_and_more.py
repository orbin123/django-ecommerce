# Generated by Django 5.1.7 on 2025-04-07 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="city",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="profile",
            name="country",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="profile",
            name="state",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
