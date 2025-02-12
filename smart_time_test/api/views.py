from http import HTTPStatus

from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.request_models import Register
from api.serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        request_data = request.json()

        try:
            Register.model_validate(request_data)
        except ValidationError:
            response = {
                "status": "error",
                "description": "Request data isn't valid",
            }
            return Response(data=response, status=HTTPStatus.BAD_REQUEST)

        if User.objects.filter(email=request_data["email"]).exists():
            response = {
                "status": "error",
                "description": "User already registered",
            }
            return Response(data=response, status=HTTPStatus.BAD_REQUEST)

        User.objects.create(**request_data)

        response = {"status": "ok", "description": "User already registered"}
        return Response(data=response, status=HTTPStatus.BAD_REQUEST)


class UserView(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()

        if not user:
            response = {"description": "User not found"}
            return Response(data=response, status=HTTPStatus.NOT_FOUND)

        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data)
