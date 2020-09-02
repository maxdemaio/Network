from datetime import datetime
import json

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage
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
        newPostForm = PostForm()

        # Pagination of posts
        # Sort the posts from most recent to oldest
        allPosts = Posts.objects.order_by('time_posted')
        paginator = Paginator(allPosts, 2) # Two per page
        page_number = request.GET.get('page', 1)

        print("Number of Pages")
        print(paginator.num_pages)

        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            page_obj = paginator.get_page(1)

        # Toggle edit buttons based on if user ids match the post's poster
        if request.user.is_authenticated == True:
            currentUserID = User.objects.get(username=request.user).id
        else:
            currentUserID = None

        return render(request, "network/index.html", {
            "newPostForm": newPostForm,
            "currentUserID": currentUserID,
            "page_obj": page_obj
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
    profileUserID = User.objects.get(username=user).id
    userPosts = Posts.objects.filter(user_id=profileUserID)

    # TODO
    # Get following/follower count for current user
    following = UserFollowing.objects.filter(user_id=profileUserID)
    print(following)

    # Toggle edit buttons based on if user ids match the post's poster
    if request.user.is_authenticated == True:
        # Check if user logged in is the same user as the profile
        # If they are the same, do not display a follow button
        currentUserID = User.objects.get(username=request.user).id
        if User.objects.get(username=request.user).id == profileUserID:
            followButton = False
        else:
            followButton = True
    else:
        currentUserID = None
        followButton = False

    return render(request, "network/profile.html", {
        "user": user,
        "userPosts": userPosts,
        "followButton": followButton,
        "currentUserID": currentUserID
    })


# AJAX routes
def editPost(request):
    """ Update the contents of a post based on AJAX id and contents """
    if request.method == "POST":
        post_id = int(request.POST.get('postID', ''))
        newContents = request.POST.get("content", "")
        print(post_id)
        print(newContents)
        
        # Update post w/ given post ID with new contents
        p = Posts.objects.get(id=post_id)
        p.content = newContents  # change field
        p.save()  # this will update only

        # Pass back success
        return HttpResponse(json.dumps({'response': 'success'}), content_type='application/json')


def toggleFollow(request):
    """ Update the follower / followee table """
    if request.method == "POST":
        # Check and make sure user is valid again
        if request.user.is_authenticated == True:
            currentUserID = User.objects.get(username=request.user).id
            print(currentUserID)
        else:
            return HttpResponse("You must be signed in to follow another user")
        
        follower = "examplePerson"
        followee = "examplePerson2"

        # TODO Obtain following_user ID
        # UserFollowing.objects.create(user_id=currentUserID,
        #                              following_user_id=follow.id)
        # Pass back success
        return HttpResponse(json.dumps({'response': 'success'}), content_type='application/json')
