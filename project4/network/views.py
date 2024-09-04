import json
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django import forms

from .models import User,Postare,Follow

class PostareForm(forms.Form):
    body = forms.CharField(
        label = "New Post:",
        widget=forms.Textarea(attrs={
            'style': 'width: 100%; height: 200px;', 
            'placeholder': 'Write your post here...'
        }))

@csrf_exempt
def index(request):
    form = PostareForm()
    return render(request, "network/index.html", {"form" : form})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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

@login_required
def save_post(request):
    if request.method == "POST":
        form = PostareForm(request.POST)
        if form.is_valid():
            post_body = form.cleaned_data["body"]
            try:
                newPost = Postare(
                    user = request.user,
                    body = post_body
                )
            except:
                return HttpResponseRedirect(reverse("index"))
            newPost.save()
            print("Saved")
    return HttpResponseRedirect(reverse("index"))

def get_posts(request,post_type):
    if post_type == "All":
        try:
            posts = Postare.objects.order_by('-timestamp').all()
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            serialized_posts = [post.serialize() for post in page_obj]
            return JsonResponse({'data': serialized_posts,'total_pages' : paginator.num_pages,'logged_user' : request.user.username}, safe=False)
        except:
            return JsonResponse({"error": "No posts/error with the request"}, status=400)
    else:
        try:
            user = User.objects.get(username=post_type)
            user_posts = Postare.objects.filter(user = user).order_by('-timestamp')
            user_paginator = Paginator(user_posts, 10)
            user_page_number = request.GET.get('page')
            user_page_obj = user_paginator.get_page(user_page_number)
            serialized_posts = [post.serialize() for post in user_page_obj]
            return JsonResponse({'data': serialized_posts,'total_pages' : user_paginator.num_pages,'logged_user' : request.user.username}, safe=False)
        except:
            return JsonResponse({"error": "No posts/error with the request"}, status=400)


def get_user(request,usr):
    try:
        if request.user.is_authenticated:
            follower = User.objects.get(username=request.user)
        following = User.objects.get(username=usr)
    except:
        return HttpResponse("invalid user")
    try:
        follow = Follow.objects.get(follower=follower,followed=following)
        is_following = 1
    except:
        is_following = 0
    try:
        follower_count = Follow.objects.filter(followed=following).count()
        following_count = Follow.objects.filter(follower=following).count()
    except:
        print("somethin went wrog")
        follower_count = 0
        following_count = 0
    return render(request, "network/user.html",{
        'page_user' : usr,
        'is_following' : is_following,
        "followers" : follower_count,
        "following" : following_count
        })

@csrf_exempt
def follow(request):
    if request.method == "GET":
        return JsonResponse({"error": "PUT method required"},status = 400)
    elif request.method == "PUT":

        data = json.loads(request.body)
        if data["follower"] is not None and data["follower"] is not None:
            try:
                follower = User.objects.get(username=data["follower"])
                following = User.objects.get(username=data["followed"])
            except:
                return JsonResponse({"error: Following request cannot be completed"},status = 400)
            update_follow = Follow(follower = follower,followed = following)
            update_follow.save()
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def unfollow(request):
    if request.method == "GET":
        return JsonResponse({"error" : "PUT method required"},status = 400)
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data["follower"] is not None and data["follower"] is not None:
            try:
                follower = User.objects.get(username=data["follower"])
                following = User.objects.get(username=data["followed"])
                get_follow = Follow.objects.get(follower=follower,followed=following)
            except:
                return JsonResponse({"error: Unfollow request cannot be completed"},status = 400)
            get_follow.delete()
    return HttpResponseRedirect(reverse('index'))

@login_required
def following_page(request,usr):
    return render(request, "network/following.html")

@login_required
def user_following(request):
    serialized_posts = []
    try:
        logged_user = User.objects.get(username=request.user)
        following = Follow.objects.filter(follower=logged_user)
        posts_list = []
        for follow in following:
            followed_user = User.objects.get(username=follow.followed)
            posts = Postare.objects.filter(user=followed_user)
            posts_list.extend(posts)
        paginator = Paginator(posts_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serialized_posts = [post.serialize() for post in page_obj]
        return JsonResponse({'data': serialized_posts, 'total_pages': paginator.num_pages}, safe=False)
    except:
        return JsonResponse({"error": "No posts/error with the request"}, status=400)

@csrf_exempt
def edit_post(request,id):
    if request.method == "PUT":
        post = Postare.objects.get(id=id)
        data = json.loads(request.body)
        text = data["text"]
        post.body = text
        post.timestamp = timezone.now()
        post.save()
        return JsonResponse({"Status": "Post has been edited"}, status=201)
    else:
        return JsonResponse({"error": "Post method required"}, status=400)

def get_post(request,id):
    try:
        post = Postare.objects.get(id=id)
        serialized_posts = [post.serialize()]
        return JsonResponse({'post': serialized_posts,}, safe=False)
    except:
        return JsonResponse({"error": "Error fetching request"}, status=400)

@csrf_exempt
def get_likes(request,id):
    if request.method == "PUT":
        try:
            post = Postare.objects.get(id=id)
        except:
            return JsonResponse({"error": "This post does not exist"}, status=400)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            print("liked")
            return JsonResponse({"status": "Unliked the comment"}, status=201)
        else:
            post.likes.add(request.user)
            print("unliked")
            return JsonResponse({"status": "Liked the comment"}, status=201)
        return JsonResponse({"error": "Put method required"}, status=400)

def like_count(request,id):
    try:
        post = Postare.objects.get(id=id)
        like_count = post.total_likes()
    except:
        return JsonResponse({"error": "This post does not exist"}, status=400)
    if request.user in post.likes.all():
        user_liked = 1
    else:
        user_liked = 0
    return JsonResponse({'user_liked': user_liked, 'total_likes': like_count}, safe=False)
    
    
