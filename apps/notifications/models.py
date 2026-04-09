# Django modules
from django.db.models import (
    Model, 
    ForeignKey, 
    CASCADE, 
    TextField)

# Project Modules
from apps.users.models import CustomUser
from apps.blog.models import Post
from apps.abstracts.models import Abstract


class Comment(Abstract):

    author = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        verbose_name='author',
        related_name='notification_comments'
    )

    post = ForeignKey(
        Post,
        on_delete=CASCADE,
        verbose_name="Comment's post",
    )

    body = TextField()
