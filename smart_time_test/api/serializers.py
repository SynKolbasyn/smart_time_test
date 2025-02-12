from hashlib import sha3_512

from django.db import IntegrityError
from rest_framework.serializers import (
    CharField,
    EmailField,
    Serializer,
    ValidationError,
)

from api.models import User


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
