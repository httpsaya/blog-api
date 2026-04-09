# Django Modules
from django.contrib.admin import register, ModelAdmin

# Project Modules
from .models import Comment


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = [
        'id',
        'author',
        'post',
        'body',
    ]