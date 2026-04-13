# Python modules
from typing import Any

# Django modules
from django.db.models import QuerySet, Count
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.decorators import action

# Project modules
from apps.blog.models import Post, Comment
from apps.blog.serializers import (
    PostBaseSerializer,
    PostListSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    CommentSerializer,
)

# Loggers
import logging

# Signal Modules
from .tasks import process_new_comment


logger = logging.getLogger("blog")


class PostViewSet(ViewSet):
    """
    ViewSet для обработки эндпоинтов постов без использования декораторов.
    """
    permission_classes = [IsAuthenticated]  # Добавь эту строку

    queryset = Post.objects.all()
    lookup_field = 'slug'

    def list(self, request: DRFRequest) -> DRFResponse:
        """GET posts"""

        posts = Post.objects.filter(status='published').select_related("author").annotate(
            comments_count=Count("comments")
        )

        serializer = PostListSerializer(posts, many=True)
        return DRFResponse(data=serializer.data, status=HTTP_200_OK)


    def create(self, request: DRFRequest) -> DRFResponse:
        """POST Posts"""

        if not request.user.is_authenticated:
            logger.warning("Unauthorized post creation attempt")
            return DRFResponse(status=401)

        logger.info(
            "Post creation attempt by user: %s",
            request.user.email
        )

        try:
            serializer = PostCreateSerializer(data=request.data)

            if serializer.is_valid():
                post = serializer.save(author=request.user)

                logger.info(
                    "Post created successfully: %s by %s",
                    post.title,
                    request.user.email
                )

                return DRFResponse(data=serializer.data, status=HTTP_201_CREATED)

            logger.warning(
                "Post creation failed by %s | Errors: %s",
                request.user.email,
                serializer.errors
            )

            return DRFResponse(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception:
            logger.exception(
                "Unexpected error during post creation by %s",
                request.user.email
            )
            raise


    def retrieve(self, request: DRFRequest, slug: str = None) -> DRFResponse:
        """GET Slug"""
        post = get_object_or_404(Post, slug=slug)
        serializer = PostListSerializer(post)
        return DRFResponse(data=serializer.data, status=HTTP_200_OK)


    def partial_update(self, request: DRFRequest, slug: str = None) -> DRFResponse:
        """PATCH Slug"""

        post = get_object_or_404(Post, slug=slug)

        if post.author != request.user:
            logger.warning(
                "Unauthorized update attempt on post %s by user %s",
                post.slug,
                request.user.email
            )
            return DRFResponse(
                data={"detail": "Вы не являетесь автором этого поста."},
                status=HTTP_403_FORBIDDEN
            )

        logger.info(
            "Post update attempt: %s by %s",
            post.slug,
            request.user.email
        )

        try:
            serializer = PostUpdateSerializer(post, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                logger.info(
                    "Post updated successfully: %s",
                    post.slug
                )

                return DRFResponse(data=serializer.data, status=HTTP_200_OK)

            logger.warning(
                "Post update validation failed: %s | Errors: %s",
                post.slug,
                serializer.errors
            )

            return DRFResponse(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception:
            logger.exception(
                "Unexpected error during post update: %s",
                post.slug
            )
            raise


    def destroy(self, request: DRFRequest, slug: str = None) -> DRFResponse:
        """DELETE slug"""

        post = get_object_or_404(Post, slug=slug)

        if post.author != request.user:
            logger.warning(
                "Unauthorized delete attempt on post %s by user %s",
                post.slug,
                request.user.email
            )
            return DRFResponse(status=HTTP_403_FORBIDDEN)

        logger.warning(  # delete лучше логировать как WARNING
            "Post deleted: %s by user %s",
            post.slug,
            request.user.email
        )

        try:
            post.delete()
            return DRFResponse(status=HTTP_204_NO_CONTENT)

        except Exception:
            logger.exception(
                "Unexpected error during post deletion: %s",
                post.slug
            )
            raise


    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request: DRFRequest, slug: str = None) -> DRFResponse:
        """
        GET comments
        POST comments
        """
        post = get_object_or_404(Post, slug=slug)

        if request.method == 'GET':
            comments = post.comments.select_related("author").all()
            serializer = CommentSerializer(comments, many=True)
            return DRFResponse(data=serializer.data, status=HTTP_200_OK)

        if request.method == 'POST':
            if not request.user.is_authenticated:
                logger.warning("Unauthorized comment attempt on post %s", post.slug)
                return DRFResponse(status=401)

            logger.info(
                "Comment creation attempt on post %s by %s",
                post.slug,
                request.user.email
            )

            try:
                serializer = CommentSerializer(data=request.data)

                if serializer.is_valid():
                    comment = serializer.save(author=request.user, post=post)
                    
                    process_new_comment.delay(comment.id)

                    logger.info(
                        "Comment created on post %s by %s",
                        post.slug,
                        request.user.email
                    )

                    return DRFResponse(data=serializer.data, status=HTTP_201_CREATED)

                logger.warning(
                    "Comment validation failed on post %s | Errors: %s",
                    post.slug,
                    serializer.errors
                )

                return DRFResponse(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

            except Exception:
                logger.exception(
                    "Unexpected error during comment creation on post %s",
                    post.slug
                )
                raise