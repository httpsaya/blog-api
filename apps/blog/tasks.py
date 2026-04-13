import logging
import json

# Python Modules
from datetime import timedelta

# Celery Modules
from celery import shared_task

# Django Modules
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth import get_user_model

# Project Modules
from apps.blog.models import Post
from apps.notifications.models import Comment

# Channel Modules
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


logger = logging.getLogger(__name__)

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def invalidate_posts_cache() -> None:
    cache.delete_pattern('posts:*')


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def publish_scheduled_posts() -> None:

    now = timezone.now()
    posts = Post.objects.filter(
        status=Post.Status.SCHEDULED,
        publish_at__lte=now,
    )

    channel_layer = get_channel_layer()

    for post in posts:
        post.status = Post.Status.PUBLISHED
        post.save(update_fields=['status'])

        async_to_sync(channel_layer.group_send)(
            'post_stream',
            {
                'type': 'post.message',
                'data': {
                    'post_id': post.id,
                    'title': post.title,
                    'slug': post.slug,
                }
            }
        )
        logger.info(f'Post {post.slug} published.')


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def generate_daily_stats() -> None:

    User = get_user_model()
    since = timezone.now() - timedelta(hours=24)

    new_posts = Post.objects.filter(created_at__gte=since).count()
    new_comments = Comment.objects.filter(created_at__gte=since).count()
    new_users = User.objects.filter(date_joined__gte=since).count()

    logger.info(
        f'Daily stats — posts: {new_posts}, '
        f'comments: {new_comments}, '
        f'users: {new_users}'
    )