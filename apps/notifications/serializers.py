# DRF Modules
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField
    )

# Project Module
from .models import Notification


class NotificationSerializer(ModelSerializer):

    author = CharField(
        source='comment.author.email',
        read_only=True
    )
    post_slug = CharField(
        source='comment.post.slug',
        read_only=True
    )
    post_title = CharField(
        source='comment.post.title',
        read_only=True
    )
    comment_preview = SerializerMethodField()

    class Meta:
        model=Notification
        fields = {
            'id',
            'author',
            'post_slug',
            'post_title',
            'comment_preview',
            'is_read',
            'created_at',
        }
    
    def get_comment_preview(self, obj):
        return obj.comment.body[:100]
