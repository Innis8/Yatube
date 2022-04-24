from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets 

from posts.serializers import PostSerializer
from posts.models import Post, Group, User, Follow
from posts.forms import PostForm, CommentForm


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all().select_related('group')
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    followers_count = author.following.all().count()
    following_count = author.follower.all().count()
    context = {
        'page_obj': page_obj,
        'author': author,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author=author
        ).exists()
        if profile != request.user:
            context.update({'following': following})
            return render(request, template, context)
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    author = get_object_or_404(User, username=post.author)
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    context = {
        'post': post,
        'author': author,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    groups = Group.objects.all()
    form = PostForm(request.POST, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    context = {
        'form': form,
        'groups': groups,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    if post.author_id != request.user.id:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    current_user = request.user

    if current_user != author:
        Follow.objects.get_or_create(
            user=request.user,
            author=author
        )
    return redirect(reverse('posts:profile', kwargs={'username': username}))


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    currently_follow = Follow.objects.filter(user=request.user, author=author)
    if currently_follow.exists():
        currently_follow.delete()
    return redirect(reverse('posts:profile', kwargs={'username': username}))

# def get_post(request, post_id):
#     if request.method == 'GET':
#         post = get_object_or_404(Post, pk=post_id)
#         serializer = PostSerializer(post)
#         return JsonResponse(serializer.data, safe=False)

# @api_view(['GET', 'POST'])
# def api_posts(request):
#     if request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     posts = Post.objects.all()
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def api_posts_detail(request, post_id):
#     # попробовать pk вместо pk=post_id 
#     post = get_object_or_404(Post, pk=post_id)
#     if request.method == 'PUT' or request.method == 'PATCH':
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     serializer = PostSerializer(post)
#     return Response(serializer.data)

# View-классы низкоуровневые
# class APIPost(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class APIPostDetail(APIView):
#     def get(self, request, post_id):        
#         post = get_object_or_404(Post, pk=post_id)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
    
#     def put(self, request, post_id):
#         post = get_object_or_404(Post, pk=post_id)
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, post_id):
#         post = get_object_or_404(Post, pk=post_id)
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, post_id):
#         post = get_object_or_404(Post, pk=post_id)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# View-классы на основе generics
# class APIPostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class APIPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# View-класс на основе viewsets. Делает все 6 основных операциий CRUD
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
