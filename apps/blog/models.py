# Django Modules
from django.db.models import (
    ForeignKey,
    SlugField,
    CharField,
    TextField,
    CASCADE,
    SET_NULL,
    ManyToManyField
)

# Project Modules
from apps.abstracts.models import Abstract
from settings.base import AUTH_USER_MODEL as User

class Tag(Abstract):
    """
    Tag modules
    """

    NAME_MAX_LENGTH=50

    name=CharField(
        max_length=NAME_MAX_LENGTH,
    )
    slug =SlugField(
        unique=True
    )


class Category(Abstract):
    """
    Category modules
    """

    NAME_MAX_LENGTH = 100

    name=CharField(
        max_length=NAME_MAX_LENGTH
    )

    slug = SlugField(
        unique=True
    )

    class Meta:
        verbose_name_plural = 'Categories'


class Post(Abstract):
    """
    Post modules
    """
    TITLE_MAX_LENGTH=150
    CATEGORY_MAX_LENGTH=200
    STATUS_MAX_LENGTH = 200
    STATUS_CHOICES = [
        ('draft', 'Draft',),
        ('published', 'Published'),
        ('scheduled', 'Scheduled')
    ]
    author = ForeignKey(
        to=User,
        on_delete = CASCADE
    )

    title = CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    slug = SlugField(
        unique=True,
    )

    body = TextField()

    category = ForeignKey(
        to=Category,
        on_delete = SET_NULL,
        null=True,
        max_length=CATEGORY_MAX_LENGTH,
    )

    tags = ManyToManyField(
        to=Tag,
        blank=True,
    )

    status = CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default='draft',
    )


class Comment(Abstract):
    """
    Comments modules
    """
    post = ForeignKey(
        to=Post,
        on_delete = CASCADE,
        related_name="comments"
    )
    author = ForeignKey(
        to = User,
        on_delete = CASCADE,
    )
    body = TextField()
