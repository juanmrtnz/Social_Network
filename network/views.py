from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post
from django import forms
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from django.db.models import Avg, Max, Min

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {'text': ""}
        widgets = {'text': forms.Textarea(attrs={'rows':6, 'cols':60})}
        

def paginate(request, query):
    paginator = Paginator(query, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def index(request):
    page_obj = paginate(request, Post.objects.all().order_by('-timestamp'))

    return render(request, "network/index.html", {
        'newPost_form': NewPostForm(),
        'posts': page_obj,
    })


def friends_posts(request):
    page_obj = paginate(request, Post.objects.filter(user__in=request.user.following.all()).order_by('-timestamp'))

    return render(request, 'network/friends_posts.html', {
        'posts': page_obj,
    })


def liked_posts(request):
    page_obj = paginate(request, Post.objects.filter(likes=request.user).order_by('-timestamp'))

    return render(request, 'network/liked_posts.html', {
        'posts': page_obj,
    })


def following(request):
    return render(request, 'network/following.html', {
        'users': request.user.following.all().order_by('username')
    })

def followers(request):
    return render(request, 'network/followers.html', {
        'users': request.user.followers.all().order_by('username')
    })

def profile(request, profile_username):
    page_obj = paginate(request, Post.objects.filter(user=User.objects.get(username=profile_username)).order_by('-timestamp'))

    return render(request, 'network/profile.html', {
        'profile': User.objects.get(username=profile_username),
        'posts': page_obj,
        'posts_count': len(Post.objects.filter(user=User.objects.get(username=profile_username)))
    })


def new_post(request):
    form = NewPostForm(request.POST)
    if form.is_valid():
        form_text = form.cleaned_data['text']
        new_post = Post(user=request.user, text=form_text)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Post exceeded the maximum allowed length')


@csrf_exempt
def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.user == request.user:
        data = json.loads(request.body)
        text = data.get('text', '')
        post.text = text
        if text.strip() != "":
            post.edited = True
            post.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Sneaky sneaky... hehe. Sorry, you can only do that if you are the author of the post.')


@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        if post.user == request.user:
            post.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Sneaky sneaky... hehe. Sorry, you can only do that if you are the author of the post.')


@csrf_exempt
def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def dislike(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.likes.remove(request.user)
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def follow(request, profile_username):
    user_to_follow = User.objects.get(username=profile_username)
    request.user.following.add(user_to_follow)
    user_to_follow.followers.add(request.user)
    return HttpResponseRedirect(reverse('profile', kwargs={'profile_username': profile_username}))


@csrf_exempt
def unfollow(request, profile_username):
    user_to_unfollow = User.objects.get(username=profile_username)
    request.user.following.remove(user_to_unfollow)
    user_to_unfollow.followers.remove(request.user)
    return HttpResponseRedirect(reverse('profile', kwargs={'profile_username': profile_username}))


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure username doesn't exceed maxlenght
        if len(username) > 10:
            return render(request, "network/register.html", {
                "message": "Username is too long."
            })
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
