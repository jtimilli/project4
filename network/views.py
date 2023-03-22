import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


from .models import User, Post, Following, Like

def index(request):
    posts = Post.objects.all().order_by("timestamp")
    data = []
    for post in posts:
        serialized_post = post.serialize()
        if request.user.is_authenticated:
            user_liked = Like.objects.filter(post=post, user=request.user).exists()
        else:
            user_liked = False
        serialized_post['liked'] = user_liked
        data.append(serialized_post)
    return render(request, "network/index.html", {"data": data})


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
def following(request):
    user = request.user
    following = Following.objects.filter(user=user).values_list("following", flat=True)
    posts = Post.objects.filter(user__in=following)
    return render(request, 'network/following.html', {"posts": posts})


def profile(request, username):
    user = User.objects.get(username = username)
    posts = Post.objects.filter(user = user)
    posts = posts.order_by("-timestamp")
    following = Following.objects.filter(user=user)
    followers = Following.objects.filter(following=user)
    is_following = Following.objects.filter(user=request.user, following=user).exists()

    if not following:
        followingcount = 0
    else:
        followingcount = following.count()
    
    if not followers:
        followercount = 0
    else:
        followercount = followers.count()
            
    return render(request, 'network/profile.html', {"following": is_following, "followingcount": followingcount, "followerscount": followercount, "profile": user.username, "posts": posts})



def getPost(request):
    posts = Post.objects.all()
    posts = posts.order_by("timestamp").all()
    return JsonResponse([post.seralize() for post in posts], safe=False)

@csrf_exempt
@login_required
def newPost(request):
    if request.method == "POST":
        try:
            post_content = request.POST.get("post_content")
        except IntegrityError:
            print(post_content, "Post2")
        
        if post_content == "":
            return HttpResponseRedirect(reverse("index"), {"error": "Post cant be empty"})
        else:
            user = request.user
            post = Post.objects.create(user=user, content=post_content)
            post.save()
            return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def toggleFollow(request, username):

    if request.method == "POST":
        follow = request.POST["follow"]
        user = User.objects.get(username = username)
        if follow == "follow":
            followed = Following.objects.create(user=request.user, following=user)
            followed.save()  
            return HttpResponseRedirect(reverse("profile", args=(username, )))
        elif follow == "unfollow":
            unfollow = Following.objects.filter(user=request.user, following=user)
            unfollow.delete()   
            return HttpResponseRedirect(reverse("profile", args=(username, )))
        

@csrf_exempt
def toggleLike(request, id):
    post = Post.objects.get(id=id)
    user = request.user
    if request.method == "POST":
        # check if user already liked post
        user_liked = Like.objects.filter(post=post, user=user).exists()
        # if user did like the post delete row and decrement the Post likes count
        if user_liked:
            Like.objects.filter(post=post, user=user).delete()
            post.like = int(post.like - 1)
            post.save()
            likes_count = post.like
            print(likes_count, "like count")
            return JsonResponse({"liked": False, "likes_count": likes_count})
        else:
            liked = Like.objects.create(user=user, post=post)
            post.like = int(post.like + 1)
            post.save()
            likes_count = post.like
            liked.save()
            print(post.like, "post likes")
            return JsonResponse({"liked": True, "likes_count": likes_count})
    else:
        user_liked = Like.objects.filter(post=post, user=user).exists()
        data = {'post': post.serialize(),
                'liked': user_liked,
                'likes_count': post.like}
        return JsonResponse(data)
