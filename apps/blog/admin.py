# Django Modules
from django.contrib.admin import register, ModelAdmin

# Project Modules
from .models import Post, Category


@register(Post)
class PostAdmin(ModelAdmin):
    list_display = [
        'id',
        'author',
        'title',
        'category',
    ]


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = [
        'id',
        'name',
    ]