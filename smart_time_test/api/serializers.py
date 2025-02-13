from hashlib import sha3_512

from django.db import IntegrityError
from rest_framework.serializers import (
    CharField,
    EmailField,
    Serializer,
    ValidationError,
)

from api.models import Exam, ExamRegistration, Room, Subject, User


class RegisterSerializer(Serializer):
    email = EmailField(allow_blank=False, required=True)
    password = CharField(
        min_length=8, allow_blank=False, allow_null=False, required=True
    )

    def create(self, validated_data):
        email = validated_data["email"]
        password_hash = sha3_512(
            validated_data["password"].encode()
        ).hexdigest()
        try:
            return User.objects.create(email=email, password=password_hash)
        except IntegrityError:
            raise ValidationError({"email": ["Email already in use"]})


class ExamRegisterSerializer(Serializer):
    email = EmailField(allow_blank=False, required=True)
    password = CharField(
        min_length=8, allow_blank=False, allow_null=False, required=True
    )
    subject_name = CharField(
        allow_blank=False, allow_null=False, required=True
    )
    room_number = CharField(allow_blank=False, allow_null=False, required=True)

    def create(self, validated_data):
        email = validated_data["email"]
        password_hash = sha3_512(
            validated_data["password"].encode()
        ).hexdigest()
        subject_name = validated_data["subject_name"]
        room_number = validated_data["room_number"]

        user = User.objects.filter(email=email, password=password_hash).first()
        if not user:
            message = "Email or password invalid"
            raise ValidationError({"status": "error", "description": message})

        subject = Subject.objects.filter(subject_name=subject_name).first()
        if not subject:
            message = "Subject not found"
            raise ValidationError({"status": "error", "description": message})

        room = Room.objects.filter(room_number=room_number).first()
        if not room:
            message = "Room not found"
            raise ValidationError({"status": "error", "description": message})

        exam = Exam.objects.filter(subject_id=subject, room_id=room).first()
        if not exam:
            message = "Exam not found with "
            f"subject {subject_name} and room {room_number}"
            raise ValidationError({"status": "error", "description": message})

        try:
            return ExamRegistration.objects.create(user=user, exam=exam)
        except IntegrityError:
            message = "User already registered for exam with "
            f"subject {subject_name} and room {room_number}"
            raise ValidationError({"status": "error", "description": message})
