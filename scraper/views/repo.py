from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from scraper.models import Repo
from scraper.serializers import UserSerializer, RepoSerializer
from scraper.utils import get_fields


@api_view(["GET", "DELETE", "PUT"])
def get_delete_update_repo(request, pk):
    try:
        repo = Repo.objects.get(pk=pk)
    except Repo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get a single repo
    if request.method == "GET":
        serialized_repo = RepoSerializer(repo)
        return Response(serialized_repo.data)
    # delete a single repo
    elif request.method == "DELETE":
        repo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update a single repo
    elif request.method == "PUT":
        return update_repo(repo=repo, data=request.data)


def update_repo(repo, data):
    serialized_repo = RepoSerializer(repo, data=data)
    if serialized_repo.is_valid():
        serialized_repo.save()
        return Response(serialized_repo.data, status=status.HTTP_204_NO_CONTENT)
    return Response(serialized_repo.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def get_post_repos(request):
    if request.method == "GET":
        return get_repos()
    elif request.method == "POST":
        return create_repo(request)


def get_repos():
    try:
        repos = Repo.objects.all()
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        serialized_repos = RepoSerializer(repos, many=True)
        return Response(serialized_repos.data)


def create_repo(request):
    data = {k: v for k, v in request.data.items() if k in get_fields(Repo)}
    serialized_repo = RepoSerializer(data=data)
    if serialized_repo.is_valid():
        serialized_repo.save()
        return Response(serialized_repo.data, status=status.HTTP_201_CREATED)
    return Response(serialized_repo.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_repo_owner(request, pk):
    try:
        repo = Repo.objects.get(pk=pk)
    except Repo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        serialized_repo = UserSerializer(repo.owner)
        return Response(serialized_repo.data)
