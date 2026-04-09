from django.shortcuts import render, get_object_or_404
from apps.blog.models import Post 

def get_page(request, slug):
    post = get_object_or_404(Post, slug=slug) 
    
    return render(request, 'index.html', {'post': post})