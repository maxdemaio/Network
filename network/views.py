from datetime import datetime
import json

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, UserFollowing, Posts

class PostForm(forms.Form):
    content = forms.CharField(label="Your post", max_length=300, widget=forms.Textarea)


def index(request):
    """ All Posts """
    if request.method == "POST":
        form = PostForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Check if the user is logged in
            if request.user.is_authenticated == False:
                messages.error(request, "Please register or log in to create a post")
                return HttpResponseRedirect(reverse("index"))
            else:
                # Save new post in the db, model already saves datetime
                currentUser = request.user
                content = form.cleaned_data["content"]
                newPost = Posts(user_id=currentUser.id,content=content)
                newPost.save()

                return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Error, form not valid")
    else:
        # Create new post form instance
        newPostForm = PostForm()

        # Pagination of posts
        # Sort the posts from most recent to oldest, ten per page
        allPosts = Posts.objects.order_by('time_posted')
        paginator = Paginator(allPosts, 10)
        page_number = request.GET.get('page', 1)

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


def following(request):
    """ Show posts from users the current user is following """
    # Check if user is authenticated
    if request.user.is_authenticated == True:
        currentUserID = User.objects.get(username=request.user).id
    else:
        return HttpResponse("Error, must be signed in")

    # Obtain list of people the user is following
    user = User.objects.get(id=currentUserID)
    followingSet = user.following.all()
    follower_ids = []
    for x in followingSet.values("following_user_id"):
        follower_ids.append(x["following_user_id"])

    # Pagination of posts
    # Sort the posts from most recent to oldest
    allPosts = Posts.objects.filter(user__in=follower_ids).order_by('time_posted')
    paginator = Paginator(allPosts, 2) 
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)

    return render(request, "network/following.html", {
        "currentUserID": currentUserID,
        "page_obj": page_obj
    })


def profile(request, user):
    """ Profile page for a user """
    # Get posts for current user
    profileUserID = User.objects.get(username=user).id
    userPosts = Posts.objects.filter(user_id=profileUserID)

    # Paginate user posts, ten per page
    paginator = Paginator(userPosts, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)

    # Get following/follower count for current user
    following = UserFollowing.objects.filter(user_id=profileUserID)

    # Toggle edit buttons based on if user ids match the post's poster
    if request.user.is_authenticated == True:
        # Check if user logged in is the same user as the profile
        # If they are the same, do not display a follow button
        currentUserID = User.objects.get(username=request.user).id

        # Check if user is following the user's page they are visiting
        if User.objects.get(username=request.user).id == profileUserID:
            followButton = False
        else:
            followButton = True
            try:
                followCheck = UserFollowing.objects.get(user_id=currentUserID, following_user_id=profileUserID)
                if followCheck:
                    following = True
            except UserFollowing.DoesNotExist:
                following = False
    else:
        currentUserID = None
        followButton = False

    # Display follower/following count
    profUser = User.objects.get(id=profileUserID) 
    followingCount = len(profUser.following.all())
    followerCount = len(profUser.followers.all())

    return render(request, "network/profile.html", {
        "profUser": profUser,
        "page_obj": page_obj,
        "followButton": followButton,
        "currentUserID": currentUserID,
        "following": following,
        "followingCount": followingCount,
        "followerCount": followerCount
    })


# AJAX routes
def editPost(request):
    """ Update the contents of a post based on AJAX id and contents """
    if request.method == "POST":
        post_id = int(request.POST.get('postID', ''))
        newContents = request.POST.get("content", "")
        
        # Update post w/ given post ID with new contents
        p = Posts.objects.get(id=post_id)
        p.content = newContents  # change field
        p.save()  # this will update only

        # Pass back success
        return HttpResponse(json.dumps({'response': 'success'}), content_type='application/json')


def toggleFollow(request):
    """ Update the follower / followee table """
    if request.method == "POST":
        followee = request.POST.get('followee', '')
        follow = request.POST.get("follow", False)
        followee_id = User.objects.get(username=followee).id

        # Check and make sure user is valid again
        if request.user.is_authenticated == True:
            follower = User.objects.get(username=request.user)
            follower_id = follower.id

            # Toggle follow/unfollow
            # If follow already true, change to unfollow and vise versa
            if follow == "false":
                # Unfollow
                follow_count = False
                instance = UserFollowing.objects.get(
                    user_id=follower_id, following_user_id=followee_id)
                instance.delete()
            else:
                # Follow
                follow_count = True
                UserFollowing.objects.create(
                    user_id=follower_id, following_user_id=followee_id)
                
                
            # Pass back success
            return HttpResponse(json.dumps({'response': 'success', "follow_count": follow_count}), content_type='application/json')
        else:
            return HttpResponse("You must be signed in to follow another user")

        
def toggleLike(request):
    """ Update like / like count """
    if request.method == "POST":
        # Check and make sure user is valid again
        if request.user.is_authenticated == True:
            id = int(request.POST.get('postid'))
            post = Posts.objects.get(pk=id)

            # Check if user liked post status
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(int(request.user.id))
                post.like_count = F('like_count') - 1
                post.save()
            else:
                post.likes.add(int(request.user.id))
                post.like_count = F('like_count') + 1
                post.save()
            
            post.refresh_from_db()
            result = post.like_count
            return HttpResponse(json.dumps({"result": result, "postid": id}))
        else:
            return HttpResponse("You must be signed in to like a post")
