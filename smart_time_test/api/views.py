from http import HTTPStatus

from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Exam, ExamRegistration, Room, Subject, User
from api.request_models import ExamsRegister, Register
from api.serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        try:
            Register.model_validate(request.data)
        except ValidationError:
            response = {
                "status": "error",
                "description": "Request data isn't valid",
            }
            return Response(data=response, status=HTTPStatus.BAD_REQUEST)

        if User.objects.filter(email=request.data["email"]).exists():
            response = {
                "status": "error",
                "description": "User already registered",
            }
            return Response(data=response, status=HTTPStatus.BAD_REQUEST)

        User.objects.create(**request.data)

        response = {
            "status": "ok",
            "description": "User successfully registered",
        }
        return Response(data=response, status=HTTPStatus.OK)


class ExamsRegisterView(APIView):
    def post(self, request):
        try:
            ExamsRegister.model_validate(request.data)
        except ValidationError:
            response = {
                "status": "error",
                "description": "Request data isn't valid",
            }
            return Response(data=response, status=HTTPStatus.BAD_REQUEST)

        user = User.objects.filter(email=request.data["user_email"]).first()

        if not user:
            response = {"status": "error", "description": "User not found"}
            return Response(data=response, status=HTTPStatus.NOT_FOUND)

        exams = []

        for exam in request.data["exams"]:
            subject = Subject.objects.filter(
                subject_name=exam["subject_name"]
            ).first()
            if not subject:
                response = {
                    "status": "error",
                    "description": "Subject not found",
                }
                return Response(data=response, status=HTTPStatus.NOT_FOUND)

            room = Room.objects.filter(room_number=exam["room_number"]).first()
            if not room:
                response = {"status": "error", "description": "Room not found"}
                return Response(data=response, status=HTTPStatus.NOT_FOUND)

            exam = Exam.objects.filter(
                subject_id=subject.id, room_id=room.id
            ).first()
            if not exam:
                response = {"status": "error", "description": "Exam not found"}
                return Response(data=response, status=HTTPStatus.NOT_FOUND)

            exams.append(exam)

        for exam in exams:
            ExamRegistration.objects.create(exam=exam.id, user=user.id)

        response = {
            "status": "ok",
            "description": "User successfully registered to exams",
        }
        return Response(data=response, status=HTTPStatus.OK)


class UserView(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()

        if not user:
            response = {"description": "User not found"}
            return Response(data=response, status=HTTPStatus.NOT_FOUND)

        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data)
