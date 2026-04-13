# Celery Modules
from celery import shared_task

# Project Modules
from apps.notifications.models import Notification, Comment

# Channel Modules
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def process_new_comment(comment_id: int) -> None:

    comment = Comment.objects.select_related(
        'post__author', 'author'
    ).get(id=comment_id)

    post_author = comment.post.author

    if comment.author == post_author:
        return

    Notification.objects.create(
        recipient=post_author,
        comment=comment,
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'post_stream',
        {
            'type': 'post.message',
            'data': {
                'comment_id': comment.id,
                'post_slug': comment.post.slug,
                'author': comment.author.email,
            }
        }
    )