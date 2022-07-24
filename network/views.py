import json
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.core.paginator import Paginator

from .models import User, Post, Profile


def index(request):
    allPosts = Post.objects.order_by("-timestamp").all()
    liked = []

    #isolate the liked posts.
    for post in allPosts:
        for i in post.liked_by.all():
            if request.user == i:
                liked.append(post.id)

    return render(request, "network/index.html", {
        'posts': allPosts,
        'liked_posts': liked
    })


@login_required
def user_profile(request, username):

    personalPosts = Post.objects.filter(username=username)
    profile_info = Profile.objects.filter(username=username).annotate(
        follower_count=Count("followers", distinct=True),
        following_count=Count("following", distinct=True)
    ).values()[0]

    profile_info["posts"]=list(personalPosts.values())

    print(profile_info)

    liked = []

    # isolate the liked posts.
    for post in personalPosts:
        for i in post.liked_by.all():
            if request.user == i:
                liked.append(post.id)

    return render(request, "network/user_profile.html", {
        'posts': personalPosts,
        'liked_posts': liked,
        'profile_info': profile_info
    })



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
        user_bio = request.POST["user_bio"]

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
            print("Here",user.username)
            newProfile = Profile(
                user=user,
                username=username,
                user_bio=user_bio
            )

            newProfile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def create_post(request):
    print(request.user)
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    content = json.loads(request.body)
    newPost= Post(
            user=request.user,
            body=content["body"],
            username=request.user
        )

    newPost.save()

    return JsonResponse({"message": "saved successfully."}, status=201)

@login_required
def personal_profile(request):
    personalPosts = Post.objects.filter(user=request.user)

    profile_info = Profile.objects.filter(username=request.user).annotate(
        follower_count=Count("followers", distinct=True),
        following_count=Count("following", distinct=True)
    ).values()[0]

    print(profile_info)

    return render(request, "network/personal_profile.html",{
        'posts': personalPosts,
        'profile_info': profile_info
    })

@login_required
def likes(request, id):

        try:
            post = Post.objects.get(id=id)
        except:
            return JsonResponse({"error": "Post does not exist."}, status=400)

        like_users = post.liked_by
        like_user = like_users.filter(username=request.user)
        if like_user:
            like_users.remove(request.user)
            like_count = post.like_count - 1
            post.like_count = like_count
            post.save()
            return JsonResponse({"like_count": like_count, "title": "Like"}, status=200)
        else:
            like_users.add(request.user)
            like_count = post.like_count + 1
            post.like_count = like_count
            post.save()
            return JsonResponse({"like_count": like_count, "title": "Unlike"}, status=200)


def following_posts(request):
    following = Profile.objects.get(user=request.user).following.all()

    posts = Post.objects.filter(user__in=following)

    return render(request, "network/Following_posts.html", {
        'posts': posts
    })


def postEdit(request, id):
        current_post = Post.objects.get(id=id)
        print(current_post)
        return render(request, "network/post_edit.html")

# add to user following list
@login_required
def follow(request, username):

    try:
        follwing_profile = Profile.objects.get(username=username)
        follwer_profile = Profile.objects.get(username=request.user)
        user = User.objects.get(username=username)
        print(user)
    except:
        return JsonResponse({"error": "Post does not exist."}, status=400)

    following_users = follwing_profile.followers
    followed_users = follwer_profile.following
    following_user = following_users.filter(username=request.user)
    followed_user = followed_users.filter(username=username)
    if following_user or followed_user:
        following_users.remove(request.user)
        followed_users.remove(user)
        follwing_profile.save()
        follwer_profile.save()
        return redirect("index")
    else:
        following_users.add(request.user)
        followed_users.add(user)
        follwing_profile.save()
        follwer_profile.save()
        return redirect("index")

