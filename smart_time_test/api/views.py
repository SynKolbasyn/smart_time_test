from http import HTTPStatus

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Exam, ExamRegistration, User
from api.serializers import (
    ExamRegisterSerializer,
    ExamSrializer,
    ExamUnregisterSerializer,
    RegisterSerializer,
    UserSerializer,
)


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


class ExamRegisterView(APIView):
    def post(self, request):
        serializer = ExamRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "status": "ok",
            "description": "User successfully registered for exam",
        }
        return Response(data=response, status=HTTPStatus.OK)


class ExamUnregisterView(APIView):
    def delete(self, request):
        serializer = ExamUnregisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        room_number = serializer.validated_data["room_number"]

        ExamRegistration.objects.filter(
            user__email=email, exam__room_id__room_number=room_number
        ).delete()

        response = {
            "status": "ok",
            "description": "User successfully unregistered for exam",
        }
        return Response(data=response, status=HTTPStatus.OK)


class ExamsView(ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSrializer


class UserView(APIView):
    def get(self, request, id):
        serializer = UserSerializer(data={"id": id})
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(id=id).first()

        exam_registrations = ExamRegistration.objects.filter(user=user)
        data = {"user": user, "exams": [p.exam for p in exam_registrations]}
        exams = UserSerializer(data)

        return Response(data=exams.data)
