from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from scraper.models import User
from scraper.serializers import UserSerializer, RepoSerializer
from scraper.utils import get_fields


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
    data = {k: v for k, v in request.data.items() if k in get_fields(User)}
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
