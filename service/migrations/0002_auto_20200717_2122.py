# Generated by Django 3.0.8 on 2020-07-17 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="repo", name="created_at",),
        migrations.RemoveField(model_name="repo", name="updated_at",),
        migrations.AddField(
            model_name="repo",
            name="archived",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="repo",
            name="clone_url",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="default_branch",
            field=models.CharField(default="master", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="disabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="repo",
            name="forks",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="forks_count",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="git_url",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="has_downloads",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="repo",
            name="has_issues",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="repo",
            name="has_pages",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="repo",
            name="has_projects",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="repo",
            name="has_wiki",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="repo",
            name="homepage",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="language",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="license",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="mirror_url",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="open_issues",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="open_issues_count",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="size",
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="ssh_url",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="stargazers_count",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="svn_url",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="watchers",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repo",
            name="watchers_count",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
