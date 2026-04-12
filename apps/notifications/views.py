# Python Modules
import asyncio
import json

# Django Modules
from django.http.response import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404

# Project Modules
from apps.blog.models import Post 

# Channel Modules
from channels.layers import get_channel_layer


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
