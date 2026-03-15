# Rest Framework
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

# Project Modules
from apps.blog.models import (
    Post, Comment,
    Category, Tag)
from apps.abstracts.serializers import CustomUserForeignSerializer

# Loggers
import logging
logger = logging.getLogger("blog")


class PostBaseSerializer(ModelSerializer):
    """
    Base serializer for Posts
    """
    class Meta:
        model =Post
        fields = "__all__"


class PostListSerializer(PostBaseSerializer):
    """
    Serializer for listing Post instances with count of comments and author details.
    """

    author = CustomUserForeignSerializer(read_only=True)
    comments_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "slug",
            "author",
            "status",
            "comments_count",
            "created_at",
        )

    def get_comments_count(self, obj: Post) -> int:
        """
        Get the count of comments associated with the post.
        """
        return getattr(obj, "comments_count", obj.comments.count())


class PostCreateSerializer(PostBaseSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'slug',
            'author',
            'status',
        )

    def create(self, validated_data):
        logger.debug(
            "Creating post with title: %s",
            validated_data.get("title")
        )

        try:
            post = super().create(validated_data)

            logger.info(
                "Post created in serializer: %s (ID: %s)",
                post.title,
                post.id
            )

            return post
        except Exception:
            logger.exception(
                "Unexpected error while creating post: %s",
                validated_data.get("title")
            )
            raise


class PostUpdateSerializer(PostBaseSerializer):

    class Meta:
        model = Post
        fields = (
            'title',
            'category'
            'tag',
            'status',
        )

    def update(
            self,
            instance,
            validated_data
    ):
        logger.debug(
            "Updating post: %s (ID: %s)",
            instance.slug,
            instance.id
        )
        try:
            post = super().update(instance, validated_data)

            logger.info(
                "Post updated in serializer: %s (ID: %s)",
                post.slug,
                post.id
            )

            return post

        except Exception:
            logger.exception(
                "Unexpected error while updating post: %s",
                instance.slug
            )
            raise


class CommentSerializer(PostBaseSerializer):
    author = CustomUserForeignSerializer(read_only=True)

    class Meta:

        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "body",
            "created_at",
        )
        read_only_fields = ("id", "post", "author", "created_at")

    def create(self, validated_data):
        logger.debug("Creating comment")

        try:

            comment = super().create(validated_data)

            logger.info(
                "Comment created (ID: %s) for post ID: %s",
                comment.id,
                comment.post.id
            )

            return comment

        except Exception:
            logger.exception("Unexpected error while creating comment")
            raise
