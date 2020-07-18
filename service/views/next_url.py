from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from service.models import NextUrl
from service.serializers import NextUrlSerializer
from service.utils import get_fields_of_model


@api_view(["GET", "DELETE", "PUT"])
def get_delete_update_next_link(request, entity):
    if entity.upper() not in ["REPO", "USER"]:
        return Response(
            {"error": "Invalid entity, valid values are 'REPO' or 'USER'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        next_url = NextUrl.objects.get(entity=entity.upper())
    except NextUrl.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serialized_url = NextUrlSerializer(next_url)
        return Response(serialized_url.data)
    elif request.method == "DELETE":
        next_url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        serialized_url = NextUrlSerializer(next_url, data=request.data)
        if serialized_url.is_valid():
            serialized_url.save()
            return Response(serialized_url.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serialized_url.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def get_post_next_links(request):
    if request.method == "GET":
        return get_next_links()
    elif request.method == "POST":
        return create_next_link(request)


def get_next_links():
    try:
        urls = NextUrl.objects.all()
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        serialized_urls = NextUrlSerializer(urls, many=True)
        return Response(serialized_urls.data)


def create_next_link(request):
    data = {k: v for k, v in request.data.items() if k in get_fields_of_model(NextUrl)}
    serialized_url = NextUrlSerializer(data=data)
    if serialized_url.is_valid():
        serialized_url.save()
        return Response(serialized_url.data, status=status.HTTP_201_CREATED)
    return Response(serialized_url.errors, status=status.HTTP_400_BAD_REQUEST)
