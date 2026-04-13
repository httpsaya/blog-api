# Python Modules
from typing import Any

# Django Modules
from django.db.models.signals import post_save
from django.dispatch import receiver

# Project Modules
from apps.blog.models import Post
from .models import Comment, Notification

# Channel Modules
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Post)
def notify_post(
    sender, 
    instance, 
    created, 
    **kwargs: dict[str, Any]
    ):
    channel_layer = get_channel_layer()

    payload = {
        'post_id': instance.id,
        'title': instance.title,
        'slug': instance.slug,
        'author': {
            'id': instance.author.id,
            'email': instance.author.email,
        },
        'created_at': instance.created_at.isoformat()
    }
    async_to_sync(channel_layer.group_send)(
        'post_stream',{
            'type': 'post.message',
            'data': payload
        }
    )


@receiver(post_save, sender=Comment)
def create_notification(
    sender, 
    instance, 
    created, 
    **kwargs: dict[str, Any]
    ):
    """
    Create a Notification whenever a new Comment is saved
    """

    if not created:
        return
    
    post_author = instance.post.author
    if instance.author == post_author:
        return 
    
    Notification.objects.create(
        recipient=post_author,
        comment=instance
    )