from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ExamRegisterSerializer, RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "status": "ok",
            "description": "User successfully registered",
        }
        return Response(data=response, status=HTTPStatus.OK)


class ExamsRegisterView(APIView):
    def post(self, request):
        serializer = ExamRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "status": "ok",
            "description": "User successfully registered for exam",
        }
        return Response(data=response, status=HTTPStatus.OK)
