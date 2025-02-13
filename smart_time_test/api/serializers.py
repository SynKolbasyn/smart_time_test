from hashlib import sha3_512

from django.db import IntegrityError
from rest_framework.serializers import (
    CharField,
    EmailField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SlugRelatedField,
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
    room_number = IntegerField(allow_null=False, required=True)

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


class ExamUnregisterSerializer(Serializer):
    email = EmailField(allow_blank=False, required=True)
    password = CharField(
        min_length=8, allow_blank=False, allow_null=False, required=True
    )
    subject_name = CharField(
        allow_blank=False, allow_null=False, required=True
    )
    room_number = IntegerField(allow_null=False, required=True)

    def is_valid(self, *, raise_exception=False):
        result = super().is_valid(raise_exception=raise_exception)

        email = self.validated_data["email"]
        password_hash = sha3_512(
            self.validated_data["password"].encode()
        ).hexdigest()
        subject_name = self.validated_data["subject_name"]
        room_number = self.validated_data["room_number"]

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

        exam_registration = ExamRegistration.objects.filter(
            user=user, exam=exam
        ).first()
        if not exam_registration:
            message = "User not registered for exam with "
            f"subject {subject_name} and room {room_number}"
            raise ValidationError({"status": "error", "description": message})

        return result


class ExamSrializer(ModelSerializer):
    room_number = SlugRelatedField(
        slug_field="room_number", queryset=Room.objects.all(), source="room_id"
    )
    subject_name = SlugRelatedField(
        slug_field="subject_name",
        queryset=Subject.objects.all(),
        source="subject_id",
    )

    class Meta:
        model = Exam
        fields = ("id", "subject_name", "room_number")
