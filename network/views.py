import json
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

from .models import User, Post, Profile


def index(request):
    allPosts = Post.objects.order_by("-timestamp").all()

    return render(request, "network/index.html", {
        'posts': allPosts,

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

    return JsonResponse(profile_info, safe=False)



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
    post = Post.objects.filter(id=id).values()

    print(post)

    return JsonResponse({"message": "saved successfully."}, status=201)






