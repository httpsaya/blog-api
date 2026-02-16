# Django Modules
from typing import Any
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    DateTimeField,
    ImageField
)
from django.contrib.auth.models import BaseUserManager

# Project Modules
from apps.abstracts.models import Abstract

class CustomUserManager(BaseUserManager):
    """
    Custom User's Manager Panel
    """
    def __obtain_the_user(
            self,
            email: str,
            first_name: str,
            last_name: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> "CustomUser":
        if not email:
            raise ValidationError(
                message="no email"
            )
        if not password:
            raise ValidationError(
                message="no password"
            )
        if not first_name:
            raise ValidationError(
                message="no first name"
            )
        if not last_name:
            raise ValidationError(
                message="no last name"
            )

        new_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name = first_name,
            last_name=last_name,
            **kwargs,
        )
        return new_user


    def create_superuser(
            self,
            email: str,
            first_name: str,
            last_name: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        new_user: 'CustomUser' = self.__obtain_the_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        if password:
            new_user.set_password(password)
        else:
            new_user.set_password('sayacpp0406')

        new_user.save(using=self._db)
        return new_user


    def create_user(
            self,
            email: str,
            first_name: str,
            last_name: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        new_user: 'CustomUser' = self.__obtain_the_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )
        if password:
            new_user.set_password(password)
        else:
            new_user.set_password('sayacpp0406')

        new_user.save(using=self._db)
        return new_user


class CustomUser(AbstractBaseUser, PermissionsMixin, Abstract):
    """
    Custom User Modules
    """

    FIRST_NAME_MAX_LENGTH = 50
    EMAIL_MAX_LENGTH = 200
    PASSWORD_MAX_LENGTH = 200

    email = EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        db_index=True,
        verbose_name="Email Field",
        help_text="User's email addresses",
    )

    first_name = CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        verbose_name="First Name",
    )
    last_name = CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        verbose_name="Last Name",
    )

    is_active = BooleanField(
        default=True,
        verbose_name="Active Status",
    )

    is_staff = BooleanField(
        default=False,
        verbose_name="Is The User Admin?"
    )

    date_joined = DateTimeField(
        auto_now_add=True
    )

    avatar = ImageField(
        null=True,
        blank=True
    )
    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
        # validators=[validate_password],
        verbose_name="Password",
        help_text="User's hash representation of the password",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:

        verbose_name = 'Custom user'
        verbose_name_plural = "Custom Users"
        ordering = ["-created_at"]

    def clean(self) -> None:
        return super().clean()