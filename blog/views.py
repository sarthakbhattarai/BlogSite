from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Comment, Category, Tag
from django.db.models import Q

# Homepage View
def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    paginator = Paginator(posts, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

# Post Detail View
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(approved=True)
    if request.method == 'POST':
        comment_author = request.POST.get('author')
        comment_content = request.POST.get('content')
        if comment_author and comment_content:
            Comment.objects.create(post=post, author=comment_author, content=comment_content)
            return redirect('post_detail', slug=post.slug)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

# Search View
def post_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'blog/post_search.html', {'results': results, 'query': query})