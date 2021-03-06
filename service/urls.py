from django.conf.urls import include, url
from rest_framework import routers
from service import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"repos", views.RepoViewSet)

urlpatterns = [
    url("", include(router.urls)),
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
    url(r"^api/v1/scrape_github", views.scrape_github, name="scrape_github"),
    url(
        r"^api/v1/scrape_user_repos/(?P<username>[A-Za-z]+)$",
        views.scrape_user_repos,
        name="scrape_user_repos",
    ),
]
