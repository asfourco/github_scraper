from django.conf.urls import url, include
from service import views


urlpatterns = [
    url(
        r"^api/v1/users/(?P<pk>[0-9]+)$",
        views.get_delete_update_user,
        name="get_delete_update_user",
    ),
    url(r"^api/v1/users/$", views.get_post_users, name="get_post_users"),
    url(
        r"^api/v1/users/(?P<pk>[0-9]+)/repos/$",
        views.get_repos_of_user,
        name="get_repos_of_user",
    ),
    url(
        r"^api/v1/repos/(?P<pk>[0-9]+)$",
        views.get_delete_update_repo,
        name="get_delete_update_repo",
    ),
    url(r"^api/v1/repos/$", views.get_post_repos, name="get_post_repos"),
    url(
        r"^api/v1/repos/(?P<pk>[0-9]+)/owner/$",
        views.get_repo_owner,
        name="get_repo_owner",
    ),
    url(
        r"^api/v1/next_url/(?P<entity>[A-Za-z]+)$",
        views.get_delete_update_next_link,
        name="get_delete_update_next_link",
    ),
    url(r"^api/v1/next_url/$", views.get_post_next_links, name="get_post_next_links"),
    url(r"^api/v1/scrape_github", views.scrape_github, name="scrape_github"),
    url(
        r"^api/v1/scrape_user_repos/(?P<username>[A-Za-z]+)$",
        views.scrape_user_repos,
        name="scrape_user_repos",
    ),
]
