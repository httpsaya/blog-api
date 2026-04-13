# Channel Modules
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# Priject Modules
from apps.notifications.models import Comment

class CommentConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.slug = self.scope['url_route']['kwargs']['slug']
        self.comment_group_name = f'comment_{self.slug}'

        await self.channel_layer.group_add(
            self.comment_group_name,
            self.channel_name,
        )

        await self.accept()

        old_comments = await self.get_comments()
        for comment in old_comments:
            await self.send(text_data=json.dumps({
                'author': comment['author__email'],
                'body': comment['body']
            }))
    

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.comment_group_name,
            self.channel_name
        )
    

    async def receive(self, text_data = None):

        data = json.loads(text_data)

        if not self.scope['user'].is_authenticated:
            await self.close()
            return
        
        author=self.scope['user']
        body = data['data']
        post = await self.get_post()

        await self.save_comment(author, body, post)

        await self.channel_layer.group_send(
            self.comment_group_name, {
                'type': 'new_comment',
                'author': author.email,
                'body': body,
            }
        )


    async def new_comment(self, event):
        body = event['body']
        author = event['author']

        await self.send(text_data=json.dumps({
            'author': author,
            'body': body
        }))


    @sync_to_async
    def get_post(self):
        from apps.blog.models import Post
        return Post.objects.get(slug=self.slug)


    @sync_to_async
    def get_comments(self):
        return list(
            Comment.objects.filter(post__slug=self.slug)
            .order_by('created_at')
            .values('author__email', 'body')
        )


    @sync_to_async
    def save_comment(self, author_email, body, post):
        Comment.objects.create(
            author=author_email,
            body=body,
            post=post
        )