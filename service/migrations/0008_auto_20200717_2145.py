# Generated by Django 3.0.8 on 2020-07-17 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0007_auto_20200717_2135"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repo", name="git_url", field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="repo",
            name="homepage",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="repo",
            name="mirror_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="repo", name="ssh_url", field=models.CharField(max_length=200),
        ),
    ]
