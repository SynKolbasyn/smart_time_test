from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.serializers import UserSerializer


class UserView(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()

        if not user:
            response = {"description": "User not found"}
            return Response(data=response, status=HTTPStatus.NOT_FOUND)

        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data)
