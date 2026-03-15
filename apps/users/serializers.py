# Python modules
from typing import Any, Optional

# Django Rest Framework
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    Serializer,CharField,EmailField
)
# Project Modules
from apps.users.models import CustomUser

# Loggers
import logging
logger = logging.getLogger("users")

class UserRegistrationSerializer(Serializer):
    """
    user's registration serializer
    """
    email = EmailField(
        required=True,
        max_length=CustomUser.EMAIL_MAX_LENGTH
    )
    first_name = CharField(
        required=True,
        max_length=CustomUser.FIRST_NAME_MAX_LENGTH
    )
    last_name = CharField(
        required=True,
        max_length=CustomUser.FIRST_NAME_MAX_LENGTH
    )
    password = CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields={
            'email',
            "password",
            "first_name",
            "last_name",
        }
    def validate(
            self,
            attrs: dict[str, Any],) ->  dict[str, Any]:

        email = attrs.get('email')

        logger.debug("Validating registration for email: %s", email)

        if CustomUser.objects.filter(email=email).exists():
            logger.warning("Registration failed - email already exists: %s", email)
            raise ValidationError({
                "email": "User with this email already exists"
            })
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        logger.debug("Creating user with email: %s", email)

        user=CustomUser.objects.create_user(**validated_data)
        logger.info("User created successfully in serializer: %s", user.email)

        return user


class UserLoginSerializer(Serializer):
    """
    user's login serializer
    """
    email = EmailField(
        required=True,
        max_length=CustomUser.EMAIL_MAX_LENGTH
    )
    password = CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields={
            'email',
            "password",
        }
    def validated_email(
            self,
            value: str,
    ) -> str:
        return value.lower()

    def validate(
            self,
            attrs: dict[str, Any]) -> dict[str, Any]:
        email: str = attrs['email']
        password: str = attrs["password"]

        logger.debug("Validating login for email: %s", email)

        user: Optional[CustomUser] = CustomUser.objects.filter(email=email).first()

        if not user:
            logger.warning("Login failed - user not found: %s", email)
            raise ValidationError(
                detail={
                    'email': [f'User with that email is already exists']
                }
            )

        if not user.check_password(raw_password=password):
            logger.warning("Login failed - incorrect password for: %s", email)
            raise ValidationError(
                detail={
                    'password': 'Incorrects Password'
                }
            )
        logger.debug("Login validation successful for: %s", email)
        attrs['user'] = user
        return attrs