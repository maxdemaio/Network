from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, UserFollowing, Posts

class PostForm(forms.Form):
    content = forms.CharField(label="Your post", max_length=300, widget=forms.Textarea)


def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Check if the user is logged in
            if request.user.is_authenticated == False:
                messages.error(request, "Please register or log in to create a post")
                return HttpResponseRedirect(reverse("index"))
            else:
                # Save new post in the db
                currentUser = request.user
                content = form.cleaned_data["content"]

                # datetime object containing current date and time
                now = datetime.now()
                newPost = Posts(user_id=currentUser.id,content=content)
                newPost.save()

                print(content)
                print(currentUser.id)
                return HttpResponseRedirect(reverse("index"))
    else:
        # Create new post form instance
        # TODO sort the posts from most recent to oldest
        newPostForm = PostForm()
        examplePosts = Posts.objects.order_by('time_posted')
        return render(request, "network/index.html", {
            "newPostForm": newPostForm,
            "examplePosts": examplePosts,
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


def profile(request, user):
    """ Profile page for a user """
    # Get posts for current user
    currentUserID = User.objects.get(username=user).id
    userPosts = Posts.objects.filter(user_id=currentUserID)

    # TODO
    # Get following/follower count for current user
    following = UserFollowing.objects.filter(user_id=currentUserID)
    print(following)

    return render(request, "network/profile.html", {
        "user": user,
        "userPosts": userPosts,
    })
