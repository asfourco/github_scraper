# Generated by Django 3.0.8 on 2020-07-18 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0022_auto_20200718_0417"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repo",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="service.User"
            ),
        ),
    ]
