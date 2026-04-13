# Django modules
from django.db.models import (
    Model, 
    ForeignKey, 
    CASCADE, 
    TextField,
    BooleanField,
    Index,
    )

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


class Notification(Abstract):

    recipient = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        related_name='notifications'
    )
    comment = ForeignKey(
        Comment,
        on_delete=CASCADE,
        related_name='notifications'
    )
    is_read = BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        indexes = [
            Index(fields=['recipient', 'is_read']),
        ]
    
    def __str__(self):
        return f'Notification for {self.recipient} on comment {self.comment_id}'
