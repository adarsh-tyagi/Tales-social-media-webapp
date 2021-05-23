from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime
from .forms import UserPostForm, ProfileUpdateForm, UserRegisterForm, UserUpdateForm, UserCommentForm
from .models import Comment, Followers, Post, Profile

# Create your views here.
# ashu qwerty@123
# aman aman@123
# admin admin

def home(request):
    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/home.html', {'posts': posts, 'count': len(posts), 'page_obj': page_obj})

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            return redirect('main:login')
        else:
            return render(request, 'main/register.html', {'form': form, 'message': 'Sign up not successful. Try again!'})
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    if request.method == 'GET':
        return render(request, 'main/login.html', {"form": AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'main/login.html', {'form': AuthenticationForm(), 'message':"No such user found!"})
        else:
            login(request, user)
            return redirect("main:home")
            
@login_required            
def user_logout(request):
    logout(request)
    return redirect("main:home")

@login_required
def user_post(request):
    if request.method == 'GET':
        return render(request, 'main/write.html', {'form': UserPostForm()})
    else:
        try:
            form = UserPostForm(request.POST)
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect("main:userpost")
        except Exception as e:
            return render(request, "main/write.html", {'form': UserPostForm(), 'message': 'Server error occurred. Try again!'})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("main:home")
        else:
            return render(request, "main/home.html", {'message': 'Profile not updated!'})
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
        curr_user = Followers.objects.get_or_create(user=request.user)
        curr = Followers.objects.get(user=request.user)
        followings = curr.another_user.all()
        followers = Followers.objects.filter(another_user=request.user)
        followers_count = len(followers)
        followings_count = len(followings)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'followers': followers,
        'followings': followings,
        'followers_count': followers_count,
        'followings_count': followings_count
    }
    return render(request, 'main/profile.html', context)

@login_required
def userpost(request):
    posts = Post.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/userpost.html', {'posts': posts, 'count': len(posts), 'page_obj': page_obj})

@login_required
def deletepost(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk, user=request.user)
    post.delete()
    return redirect("main:userpost")

@login_required
def otherprofile(request, post_user):
    follower = Followers.objects.get_or_create(user=request.user)
    post_u = get_object_or_404(User, username=post_user)
    check_follower = Followers.objects.get(user=request.user)
    is_followed = False
    if check_follower.another_user.filter(username = post_u).exists():
        is_followed = True    
    return render(request, 'main/otherprofile.html', {'user': post_u, 'is_followed': is_followed})

@login_required
def comments(request, post_obj):
    comments = Comment.objects.filter(post=post_obj).order_by('-date')
    post = get_object_or_404(Post, pk=post_obj)
    count = len(comments)
    return render(request, 'main/comments.html', {'comments': comments, 'count': count, 'post_obj': post_obj, 'post': post})

@login_required
def comment(request, post_obj):
    post = get_object_or_404(Post, pk=post_obj)
    if request.method == 'GET':
        return render(request, 'main/comment.html', {'form': UserCommentForm()})
    else:
        try:
            form = UserCommentForm(request.POST)
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            return redirect("main:home")
        except Exception as e:
            return render(request, "main/comment.html", {'form': UserCommentForm(), 'message': 'Server error occurred. Try again!'})
    
@login_required
def follow_user(request, user_name):
    other_user = User.objects.get(username = user_name)
    curr_user = Followers.objects.get(user=request.user)
    curr_user.another_user.add(other_user)
    return redirect("main:profile")

@login_required
def unfollow_user(request, user_name):
    other_user = User.objects.get(username = user_name)
    curr_user = Followers.objects.get(user=request.user)
    curr_user.another_user.remove(other_user)
    return redirect("main:profile")

@login_required
def follow_detail(request, user_name):
    curr_user = Followers.objects.get_or_create(user=request.user)
    curr = Followers.objects.get(user=request.user)
    followings = curr.another_user.all()
    followers = Followers.objects.filter(another_user=request.user)
    followers_count = len(followers)
    followings_count = len(followings)
    context = {
        'followings': followings,
        'followers': followers,
        'followers_count': followers_count,
        'followings_count': followings_count
    }
    return render(request, 'main/follow_detail.html', context)

@login_required
def other_tales(request, user_name):
    user_id = User.objects.get(username=user_name)
    posts = Post.objects.filter(user=user_id).order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={
        'posts': posts,
        'count': len(posts),
        'page_obj': page_obj
    }
    return render(request, 'main/other_tales.html', context)

@login_required
def search_user(request, user_name):
    user = User.objects.filter(username=user_name)
    if user:
        name = user_name
        return otherprofile(request, user_name)
    else:
        name = "No such user found!"
        return render(request, 'main/search_user.html', {'name': name, 'user_name': user_name})
    
@login_required
def empty_search(request):
    return redirect('main:home')