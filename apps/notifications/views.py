# Python Modules
import asyncio
import json
from typing import Any

# Django Modules
from django.http.response import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404

# Project Modules
from apps.blog.models import Post 
from apps.notifications.models import Notification
from .serializers import NotificationSerializer

# Channel Modules
from channels.layers import get_channel_layer

# DRF Modules
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import HTTP_200_OK


def get_page(request, slug):
    post = get_object_or_404(Post, slug=slug) 
    
    return render(request, 'index.html', {'post': post})


async def sse_notifications(request):
    channel_layer = get_channel_layer()

    async def event_stream():
        channel_name = await channel_layer.new_channel()
        await channel_layer.group_add('post_stream', channel_name)
        try:
            while True:
                try:
                    message = await asyncio.wait_for(
                        channel_layer.receive(channel_name),
                        timeout=30
                    )
                    if message['type'] == 'post.message':
                        data = json.dumps(message['data'])
                        yield f'data: {data}\n\n'

                except asyncio.TimeoutError:
                    yield ": ping\n\n"
        finally:
            await channel_layer.group_discard('post_stream', channel_name)
        
    return StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream',
        headers={
            'Cache-Control': "no-cache",
            'X-Accel-Buffering': 'no'
        }
    )


class NotificationViewSet(ViewSet):
    """
    GET endpoint for count Notifications
    """
    @action(
        methods=('GET',),
        detail=False,
        url_path='count',
        url_name='count',
        permission_classes = (IsAuthenticated,),
    )
    def get_count(
        self, 
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
        ) -> DRFResponse:

        unread_count: Notification = Notification.objects.filter(
            recipient = request.user,
            is_read=False,
        ).count()
        return DRFResponse({'unread_count': unread_count})
    

    @action(
        methods=('GET',),
        detail=False,
        url_path='list',
        url_name='list',
        permission_classes = (IsAuthenticated,),
    )
    def get_list(
        self, 
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
        ) -> DRFResponse:

        notifications: Notification = Notification.objects.filter(
            recipient=request.user,
        ).select_related('comment__author', 'comment__post')

        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(notifications, DRFRequest)

        serializer: NotificationSerializer = NotificationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

    @action(
        methods=('POST',),
        detail=False,
        url_path='read',
        url_name='read',
        permission_classes = (IsAuthenticated,),
    )
    def mark_read(
        self, 
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
        ) -> DRFResponse:

        updated: Notification = Notification.objects.filter(
            recipient = request.user,
            is_read=False
        ).update(is_read=True)

        return DRFResponse(
            {'marked_read': updated},
            status=HTTP_200_OK
        )