import os
from service.models import User, Repo
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from service.serializers import UserSerializer, RepoSerializer
from scraper import Scraper


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["GET"])
    def get_repos_of_user(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serialized_user = RepoSerializer(user.repo_set, many=True)
            return Response(serialized_user.data)


class RepoViewSet(viewsets.ModelViewSet):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer

    @action(detail=True, methods=["GET"])
    def get_repo_owner(self, request, pk):
        try:
            repo = Repo.objects.get(pk=pk)
        except Repo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serialized_repo = UserSerializer(repo.owner)
            return Response(serialized_repo.data)


get_delete_update_user = UserViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)

get_post_users = UserViewSet.as_view({"get": "list", "post": "create"})

get_repos_of_user = UserViewSet.as_view({"get": "get_repos_of_user"})

get_delete_update_repo = RepoViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)

get_post_repos = RepoViewSet.as_view({"get": "list", "post": "create"})

get_repo_owner = RepoViewSet.as_view({"get": "get_repo_owner"})


@api_view(["GET"])
def scrape_user_repos(request, username):
    if "per_page" in request.query_params:
        per_page = int(request.query_params.get("per_page"))
    else:
        per_page = None

    if "page" in request.query_params:
        page = int(request.query_params.get("page"))
    else:
        page = None
    sort = request.query_params.get("sort")
    type = request.query_params.get("type")
    direction = request.query_params.get("direction")
    auth_username = os.getenv("USERNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    sc = Scraper(username=auth_username, access_token=access_token)

    # check that we have this user, if not, fetch and store
    try:
        _ = User.objects.get(login=username.lower())
    except User.DoesNotExist:
        raw_user = sc.api.get_user(username=username.lower())
        serialized_user = UserSerializer(data=raw_user)
        if serialized_user.is_valid():
            serialized_user.save()

    # now fetch repos for the user and store
    try:
        response = sc.api.get_repos_of_user(
            username=username.lower(),
            per_page=per_page,
            page=page,
            type=type,
            direction=direction,
            sort=sort,
        )
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        for repo in response.get("data"):
            transformed_repo = sc.transform_repo(repo)
            sc.update_or_create_repo(data=transformed_repo)

        return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
def scrape_github(request):
    per_page = int(request.query_params.get("per_page"), 10)
    reset = request.query_params.get("reset")
    username = os.getenv("USERNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    sc = Scraper(
        per_page=per_page, reset=reset, username=username, access_token=access_token
    )

    try:
        sc.scrape()
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        return Response({"message": "Scraping successfull"}, status=status.HTTP_200_OK)
