# Generated by Django 3.0.8 on 2020-07-17 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0009_auto_20200717_2146"),
    ]

    operations = [
        migrations.CreateModel(
            name="License",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(max_length=200)),
                ("name", models.CharField(max_length=200)),
                ("spdx_id", models.CharField(max_length=200)),
                ("url", models.URLField()),
                ("node_id", models.CharField(max_length=200)),
            ],
        ),
    ]
