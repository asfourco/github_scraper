import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from service.models import User
from service.serializers import UserSerializer, RepoSerializer
from service.utils import get_fields_of_model
from scraper import Scraper


@api_view(["GET", "DELETE", "PUT"])
def get_delete_update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get a single user
    if request.method == "GET":
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)
    # delete a single user
    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update a single user
    elif request.method == "PUT":
        return update_user(user=user, data=request.data)


def update_user(user, data):
    serialized_user = UserSerializer(user, data=data)
    if serialized_user.is_valid():
        serialized_user.save()
        return Response(serialized_user.data, status=status.HTTP_204_NO_CONTENT)
    return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def get_post_users(request):
    if request.method == "GET":
        return get_users()
    elif request.method == "POST":
        return create_user(request)


def get_users():
    try:
        users = User.objects.all()
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data)


def create_user(request):
    data = {k: v for k, v in request.data.items() if k in get_fields_of_model(User)}
    serialized_user = UserSerializer(data=data)
    if serialized_user.is_valid():
        serialized_user.save()
        return Response(serialized_user.data, status=status.HTTP_201_CREATED)
    return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_repos_of_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        serialized_user = RepoSerializer(user.repos, many=True)
        return Response(serialized_user.data)


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
        new_user = {k: v for k, v in raw_user.items() if k in get_fields_of_model(User)}
        serialized_user = UserSerializer(data=new_user)
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
